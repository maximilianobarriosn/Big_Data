import com.google.api.services.bigquery.model.TableRow;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.coders.Coder;
import org.apache.beam.sdk.io.gcp.bigquery.BigQueryIO;
import org.apache.beam.sdk.io.gcp.bigquery.TableRowJsonCoder;
import org.apache.beam.sdk.io.gcp.pubsub.PubsubIO;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.*;
import org.apache.beam.sdk.transforms.windowing.FixedWindows;
import org.apache.beam.sdk.transforms.windowing.Window;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.sdk.values.PCollectionList;
import org.joda.time.Duration;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

class Config {
    JSONObject config_dict;

    public Config(String config_file_path) throws IOException {
        String json_string_config = new String(Files.readAllBytes(Paths.get(config_file_path)));
        JSONObject array = new JSONObject(json_string_config);

        config_dict = array;
    }
    public String getProject(){
        return config_dict.getJSONObject("ProjectConf").get("project").toString();
    }

    public String getDataset(){
        return config_dict.getJSONObject("ProjectConf").get("dataset").toString();
    }

    public String getTable(){
        return config_dict.getJSONObject("ProjectConf").get("table").toString();
    }

    public String getPathJsonFileSchema(){
        return config_dict.getJSONObject("ProjectConf").get("path_json_file_schema").toString();
    }

    public String getTempLocationGCS(){
        return config_dict.getJSONObject("ProjectConf").get("TempLocationGCS").toString();
    }


}
/* This class extends from DoFn to process each element and
* convert JSON string (input param) in TableRo (output). */
class ConvertJSONtoTableRow extends DoFn<String, TableRow>{
    @ProcessElement
    public void processElement(ProcessContext c) {
        // Parse the JSON into a {@link TableRow} object.
        String json = c.element();
        TableRow row_internal;
        try (InputStream inputStream =
                     new ByteArrayInputStream(json.getBytes(StandardCharsets.UTF_8))) {
            row_internal = TableRowJsonCoder.of().decode(inputStream, Coder.Context.OUTER);
        } catch (IOException e) {
            throw new RuntimeException("Failed to serialize json to table row: " + json, e);
        }
        System.out.println("##### Writing to BQ... ########");
        System.out.println(row_internal);
        c.output(row_internal);
    }
}

/*  This class implements an interface for Partition and
    allows to stablish a partition criteria.
    Receives String elements of the PCollections and
    assign an index to PCollectionList where it will be placed.
* */
class TablePartition implements Partition.PartitionFn<String> {

    @Override
    public int partitionFor(String elem, int numPartitions) {
        JSONObject obj = new JSONObject(elem);
        String table = obj.getJSONObject("source").get("table").toString();
        System.out.println(table);
        Integer output = -1;
        if (table.equals("customers1")) {
            output = 0;
        }
        if (table.equals("customers2")) {
            output = 1;
        }
        return output;
    }
}

public class CDCTest {
    /* Read a JSON File and convert it to String */
    public static String readFileAsString(String file)throws Exception
    {
        return new String(Files.readAllBytes(Paths.get(file)));
    }

    public static void main(String[] args) throws Exception {
        Config project_config = new Config("ProjectConfig.json");
        PipelineOptions options = PipelineOptionsFactory.create();
        Pipeline p = Pipeline.create(options);
        options.setTempLocation(project_config.getTempLocationGCS());
        String project = project_config.getProject();
        String dataset = project_config.getDataset();
        String table = project_config.getTable();
        String table2 = "Customer2";
        String path_json_file_schema = project_config.getPathJsonFileSchema();
        String json_table_schema = readFileAsString(path_json_file_schema);

        System.out.println(project_config.config_dict);
        // Reading JSON messages from PubSub using anonymous inner class instance (ProcessEleent and DoFn).
        PCollection<String> PJson = p.apply("Read PubSub Messages", PubsubIO.readStrings().fromSubscription("projects/cdcproject-321019/subscriptions/group_subscription_1"))
                .apply(Window.into(FixedWindows.of(Duration.standardMinutes(1))))
                .apply(ParDo.of(new DoFn<String, String>() {
                    @ProcessElement
                    public void process(ProcessContext c) {
                        c.output(c.element());
                    }
                }));

        // Partition of PCollection using TablePartition class to decide how partition is done.
        PCollectionList<String> partition = PJson.apply(Partition.of(2, new TablePartition()));

        // Get PCollections from Partitions using indexes.
        PCollection<String> Pc1= partition.get(0);
        PCollection<String> Pc2 = partition.get(1);

        // Create PCollection of Table Rows using Parallel Do.
        // ConvertJSONtoTableRow class takes an element of PCollection and convert JSON message
        // to Table Row data, this allows to insert the data in BigQuery.
        PCollection<TableRow> Pc1_table_row = Pc1.apply(ParDo.of(new ConvertJSONtoTableRow()));
        //writeToTable(project, dataset, table, json_table_schema, Pc1_table_row);

        PCollection<TableRow> Pc2_table_row = Pc2.apply(ParDo.of(new ConvertJSONtoTableRow()));
        //writeToTable(project, dataset, table2, json_table_schema, Pc2_table_row);

        p.run();
    }

    /* This method receives data from project, table and schema in BigQuery
    and a PCollection of TableRow that contains data to be inserted.
    */
    public static void writeToTable(
            String project,
            String dataset,
            String table,
            String schema,
            PCollection<TableRow> rows) {

        rows.apply(
                "Write to BigQuery",
                BigQueryIO.writeTableRows()
                        .to(String.format("%s:%s.%s", project, dataset, table))
                        .withJsonSchema(schema)
                        .withMethod(BigQueryIO.Write.Method.STREAMING_INSERTS)
                        .withoutValidation());
    }
}
