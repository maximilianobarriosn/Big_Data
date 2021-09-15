import org.apache.avro.generic.GenericData;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.transforms.Create;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.sdk.values.TypeDescriptor;
import org.apache.beam.sdk.values.TypeDescriptors;

import java.nio.channels.Pipe;
import java.util.ArrayList;
import java.util.List;

public class InmemoryExample {
    public static void main(String[] args) {

        Pipeline p = Pipeline.create();

        // Convert a Java Collection object to PCollection object.
        // Create a PCollection using a custom class Customers.
        PCollection<CustomerEntity> pList = p.apply(Create.of(getCustomers()));

        // In this basic example, map and typedescriptors are not explained. This will
        // be explained in other lessons.
        PCollection<String> pStrList = pList.apply(MapElements.into(TypeDescriptors.strings())
                                .via((CustomerEntity cust) -> cust.getName()));

        // Write in a file with csv extension and only one shard (one file).
        pStrList.apply(TextIO.write().to("./customer.csv").withNumShards(1).withSuffix(".csv"));

        p.run();
    }
    static List<CustomerEntity> getCustomers(){
        CustomerEntity c1 = new CustomerEntity("1001", "John");
        CustomerEntity c2 = new CustomerEntity("1002", "Adam");

        List<CustomerEntity> list = new ArrayList<CustomerEntity>();
        list.add(c1);
        list.add(c2);

        return list;
    }
}
