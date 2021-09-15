import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.io.mongodb.MongoDbIO;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.bson.Document;

import java.awt.image.PackedColorModel;
import java.util.HashMap;
import java.util.Map;

public class MongoDBExample {
    public static void main(String[] args) {

        Pipeline p = Pipeline.create();

        PCollection<String> pInput = p.apply(TextIO.read().from("./user_.csv"));

        PCollection<Document> pDocument = pInput.apply(ParDo.of(new DoFn<String, Document>() {

            @ProcessElement
            public void ProcessElement (ProcessContext c){

                String arr[] = c.element().split(",");

                Map<String, Object> mapDocuments = new HashMap<String, Object>();

                mapDocuments.put("userId", arr[0]);
                mapDocuments.put("OrderId", arr[1]);
                mapDocuments.put("name", arr[2]);
                mapDocuments.put("ProductId", arr[3]);
                mapDocuments.put("Amount", arr[4]);
                mapDocuments.put("Order_Date", arr[5]);
                mapDocuments.put("Country", arr[6]);

                Document d1 = new Document(mapDocuments);

                c.output(d1);
            }
        }));

        pDocument.apply(MongoDbIO.write().withUri("mongodb://localhost:27017")
                .withDatabase("training").withCollection("user"));
        p.run();
    }
}
