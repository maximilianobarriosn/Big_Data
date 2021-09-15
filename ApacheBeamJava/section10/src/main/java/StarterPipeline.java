import com.google.api.services.bigquery.model.TableFieldSchema;
import com.google.api.services.bigquery.model.TableRow;
import com.google.api.services.bigquery.model.TableSchema;
import com.sun.org.slf4j.internal.Logger;
import com.sun.org.slf4j.internal.LoggerFactory;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.io.gcp.bigquery.BigQueryIO;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;

import java.util.ArrayList;
import java.util.List;

public class StarterPipeline {
    private static final Logger LOG = LoggerFactory.getLogger(StarterPipeline.class);

    public static void main(String[] args) {

        MyOption myOptions = PipelineOptionsFactory.fromArgs(args).withValidation().as(MyOption.class);
        myOptions.setTempLocation("gs://udemy_training_max/input");
        myOptions.setStagingLocation("gs://udemy_training_max/input");
        myOptions.setProject("cdcproject-323214");

        Pipeline p = Pipeline.create(myOptions);

        List<TableFieldSchema> columns = new ArrayList<TableFieldSchema>();
        columns.add(new TableFieldSchema().setName("userId").setType("STRING"));
        columns.add(new TableFieldSchema().setName("orderId").setType("STRING"));
        columns.add(new TableFieldSchema().setName("name").setType("STRING"));
        columns.add(new TableFieldSchema().setName("productId").setType("STRING"));
        columns.add(new TableFieldSchema().setName("Amount").setType("INTEGER"));
        columns.add(new TableFieldSchema().setName("order_date").setType("STRING"));
        columns.add(new TableFieldSchema().setName("country").setType("STRING"));

        TableSchema tblSchema = new TableSchema().setFields(columns);

        PCollection<String> pInput = p.apply(TextIO.read().from("gs://udemy_training_max/input/user_.csv"));

        /* To use without BigQuery, only print data:
        pInput.apply(ParDo.of(new DoFn<String, Void>() {
            @ProcessElement
            public void processElement(ProcessContext c){

                String arr[] = c.element().split(",");

                if(arr.length==7)
                {
                    if(arr[6].equalsIgnoreCase("India")){
                        System.out.println(c.element());
                    }
                }
            }
        }));
*/
        pInput.apply(ParDo.of(new DoFn<String, TableRow>() {
            @ProcessElement
            public void processElement(ProcessContext c){

                String arr[] = c.element().split(",");

                if(arr.length==7)
                {


                    if(arr[6].equalsIgnoreCase("India")){
                        System.out.println(c.element());
                        TableRow row = new TableRow();
                        row.set("userId", arr[0]);
                        row.set("orderId", arr[1]);
                        row.set("name", arr[2]);
                        row.set("productId", arr[3]);
                        row.set("Amount", Integer.valueOf(arr[4]));
                        row.set("order_date", arr[5]);
                        row.set("country", arr[6]);

                        c.output(row);
                    }
                }
            }
        }))
                .apply(BigQueryIO.writeTableRows().to("user_order.user_table").
                        withSchema(tblSchema)
                        .withWriteDisposition(BigQueryIO.Write.WriteDisposition.WRITE_APPEND)
                        .withCreateDisposition(BigQueryIO.Write.CreateDisposition.CREATE_NEVER));

        p.run();
    }
}
