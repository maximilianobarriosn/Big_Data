import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.transforms.Filter;
import org.apache.beam.sdk.transforms.Flatten;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.sdk.values.PCollectionList;

public class FlattenExample {
    public static void main(String[] args) {
        Pipeline p = Pipeline.create();

        // Multiple pCollections flattened in one.
        PCollection<String> pCustList1 = p.apply(TextIO.read().from("./customer_1.csv"));
        PCollection<String> pCustList2 = p.apply(TextIO.read().from("./customer_2.csv"));
        PCollection<String> pCustList3 = p.apply(TextIO.read().from("./customer_3.csv"));

        PCollectionList<String> list = PCollectionList.of(pCustList1)
                                                      .and(pCustList2)
                                                      .and(pCustList3);

        PCollection<String> merged = list.apply(Flatten.pCollections());

        merged.apply(TextIO.write().to("./customer_flatten_output.csv")
                .withHeader("Id,Name,Last Name,City")
                .withNumShards(1).withSuffix(".csv"));

        p.run();
    }
}
