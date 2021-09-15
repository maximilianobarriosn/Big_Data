import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.GroupByKey;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.KV;
import org.apache.beam.sdk.values.PCollection;

// Step 2
class StringToKV extends DoFn<String, KV<String,Integer>>{

    @ProcessElement
    public void processElement(ProcessContext c){

        String input = c.element();
        String arr[] = input.split(",");

        // Get user id and amount.
        c.output(KV.of(arr[0],Integer.valueOf(arr[3])));
        System.out.println(c.element());
    }
}

// Step 4
class KVToString extends DoFn<KV<String,Iterable<Integer>>,String>{
    @ProcessElement
    public void processElement(ProcessContext c){
        String strKey= c.element().getKey();
        Iterable<Integer> vals = c.element().getValue();

        Integer sum = 0;
        for (Integer integer : vals){
            sum = sum + integer;
        }

        System.out.println(c.element());
        c.output(strKey+","+sum.toString());

    }
}

public class GroupByKeyExample {
    public static void main(String[] args) {
        Pipeline p = Pipeline.create();

        // 1 - Read CSV and convert to PCollection
        PCollection<String> pCustOrderList = p.apply(TextIO.read().from("./GroupByKey_data.csv"));

        // 2 - Convert Strings to KV
        PCollection<KV<String,Integer>> kvOrder = pCustOrderList.apply(ParDo.of(new StringToKV()));

        // 3 - Apply group by key and build KV<String, Iterable<Integer>>
        PCollection<KV<String,Iterable<Integer>>> kvOrder2 = kvOrder.apply(GroupByKey.<String, Integer>create());

        // 4 - Convert KV<String,Iterable<Integer>> to String and write.
        PCollection<String> output = kvOrder2.apply(ParDo.of(new KVToString()));

        output.apply(TextIO.write().to("./group_by_key_output.csv")
                                    .withHeader("Id,Amount")
                                    .withNumShards(1)
                                    .withSuffix(".csv"));

        p.run();
    }
}
