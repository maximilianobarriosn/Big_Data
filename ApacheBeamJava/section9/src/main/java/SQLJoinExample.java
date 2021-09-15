import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.extensions.sql.SqlTransform;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.schemas.Schema;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.sdk.values.PCollectionTuple;
import org.apache.beam.sdk.values.Row;
import org.apache.beam.sdk.values.TupleTag;

import java.util.stream.Collectors;

public class SQLJoinExample {

    final static String order_header = "userId,orderId,productId,Amount";
    final static Schema order_schema = Schema.builder().addStringField("userId")
            .addStringField("orderId")
            .addStringField("productId")
            .addDoubleField("Amount")
            .build();

    final static String user_header = "userId,name";
    final static Schema user_schema = Schema.builder().addStringField("userId")
            .addStringField("name")
            .build();

    final static Schema order_user_schema = Schema.builder().addStringField("userId")
            .addStringField("orderId")
            .addStringField("productId")
            .addDoubleField("Amount")
            .addStringField("name")
            .build();

    public static void main(String[] args) {
        Pipeline pipeline = Pipeline.create();

        // Step 1 : Read CSV file
        PCollection<String> order = pipeline.apply(TextIO.read().from("./user_order.csv"));
        PCollection<String> user = pipeline.apply(TextIO.read().from("./p_user.csv"));

        // Step 2 : Convert PCollection<String> to PCollection<Row>
        PCollection<Row> rowUserOrder = order.apply(ParDo.of(new StringToOrderRow()))
                .setRowSchema(order_schema);
        PCollection<Row> rowUser = user.apply(ParDo.of(new StringToUserRow()))
                .setRowSchema(user_schema);

        // Step 3 : Apply SqlTransform.query
        PCollection<Row> sqlInput = PCollectionTuple.of(new TupleTag<>("orders"), rowUserOrder)
                .and(new TupleTag<>("users"), rowUser)
                .apply(SqlTransform.query("select o.*, u.name from orders o inner join users u on o.userId=u.userId"));

        // Step 4 : Convert PCollection<Row> to PCollection<String>
        PCollection<String> pOutput = sqlInput.apply(ParDo.of(new RowToString()));

        pOutput.apply(TextIO.write().to("./output_beam_join_sql.csv")
                .withNumShards(1)
                .withSuffix(".csv"));

        pipeline.run();
    }

    public static class StringToOrderRow extends DoFn<String, Row> {
        @ProcessElement
        public void processElement(ProcessContext c){

            if(!c.element().equalsIgnoreCase(order_header)){
                String arr[] = c.element().split(",");
                Row record = Row.withSchema(order_schema).addValues(arr[0],arr[1],arr[2],Double.valueOf(arr[3])).build();
                c.output(record);
            }
        }
    }

    public static class StringToUserRow extends DoFn<String, Row> {
        @ProcessElement
        public void processElement(ProcessContext c){

            if(!c.element().equalsIgnoreCase(user_header)){
                String arr[] = c.element().split(",");
                Row record = Row.withSchema(user_schema).addValues(arr[0],arr[1]).build();
                c.output(record);
            }
        }
    }

    public static class RowToString extends DoFn<Row, String>{
        @ProcessElement
        public void processElement(ProcessContext c){

            String outString = c.element().getValues().stream()
                    // For left join:
                    //.filter(entity -> entity!=null)
                    .map(Object::toString).collect(Collectors.joining(","));

            c.output(outString);
        }
    }
}
