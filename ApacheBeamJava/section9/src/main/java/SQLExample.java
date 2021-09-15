import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.extensions.sql.SqlTransform;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.schemas.Schema;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.sdk.values.Row;

import java.awt.image.PackedColorModel;
import java.util.stream.Collectors;

import java.util.stream.Collectors;

public class SQLExample {

    final static String HEADER = "userId,orderId,productId,Amount";

    final static Schema schema = Schema.builder().addStringField("userId")
            .addStringField("orderId")
            .addStringField("productId")
            .addDoubleField("Amount")
            .build();

    public static void main(String[] args) {
        Pipeline pipeline = Pipeline.create();

        // Step 1 : Read CSV file
        PCollection<String> fileInput = pipeline.apply(TextIO.read().from("./user_order.csv"));

        // Step 2 : Convert PCollection<String> to PCollection<Row>
        PCollection<Row> rowInput = fileInput.apply(ParDo.of(new StringToRow())).setRowSchema(schema);

        // Step 3 : Apply SqlTransform.query
        PCollection<Row> sqlInput = rowInput.apply(SqlTransform.query("select * from PCOLLECTION"));

        // Step 4 : Convert PCollection<Row> to PCollection<String>
        PCollection<String> pOutput = sqlInput.apply(ParDo.of(new RowToString()));

        pOutput.apply(TextIO.write().to("./output_beam_sql.csv")
                .withNumShards(1)
                .withSuffix(".csv"));

        pipeline.run();
    }

    public static class StringToRow extends DoFn<String, Row> {
        @ProcessElement
        public void processElement(ProcessContext c){

            if(!c.element().equalsIgnoreCase(HEADER)){
                String arr[] = c.element().split(",");
                Row record = Row.withSchema(schema).addValues(arr[0],arr[1],arr[2],Double.valueOf(arr[3])).build();
                c.output(record);
            }
        }
    }

    public static class RowToString extends DoFn<Row, String>{
        @ProcessElement
        public void processElement(ProcessContext c){

            String outString = c.element().getValues().stream()
                    .map(Object::toString).collect(Collectors.joining(","));

            c.output(outString);
        }
    }
}
