import com.sun.org.apache.xpath.internal.operations.Bool;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.transforms.Filter;
import org.apache.beam.sdk.transforms.SerializableFunction;
import org.apache.beam.sdk.values.PCollection;

import java.io.Serializable;

class MyFilter implements SerializableFunction<String, Boolean> {

    // Use value "Los Angeles" to filter.
    @Override
    public Boolean apply(String input) {
        return input.contains("Los Angeles");
    }
}
public class FilterExample {
    public static void main(String[] args) {
        Pipeline p = Pipeline.create();

        // Filter PCollections
        PCollection<String> pCustList = p.apply(TextIO.read().from("./customer_pardo.csv"));

        PCollection<String> pOutput = pCustList.apply(Filter.by(new MyFilter()));

        pOutput.apply(TextIO.write().to("./customer_filter_output.csv")
                                    .withHeader("Id,Name,Last Name,City")
                                    .withNumShards(1).withSuffix(".csv"));

        p.run();
    }
}
