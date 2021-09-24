import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.transforms.SimpleFunction;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.sdk.values.TypeDescriptors;

class User extends SimpleFunction<String, String>{
    @Override
    public String apply(String input) {
        String arr[] = input.split(",");
        String SId = arr[0];
        String UId = arr[1];
        String Uname = arr[2];
        String VId = arr[3];
        String duration = arr[4];
        String startTime = arr[5];
        String sex = arr[6];

        String output = "";
        if(sex.equals("1")){
            output = SId + "," + UId + "," + Uname + "," + VId + "," + duration + "," + startTime + "," + "M ";
        }
        else if(sex.equals("2")){
            output = SId + "," + UId + "," + Uname + "," + VId + "," + duration + "," + startTime + "," + "F";
        }
        else
        {
            output = input;
        }
        return output;
    }
}
public class MapElementsSimpleFunction {

    public static void main(String[] args) {
        Pipeline p = Pipeline.create();

        // Convert a number of a column in a letter (1,2 -> M or F) using SimpleFunction
        PCollection<String> pUserList = p.apply(TextIO.read().from("./user.csv"));

        PCollection<String> pOutput = pUserList.apply(MapElements.via(new User()));

        pOutput.apply(TextIO.write().to("./user_output.csv").withNumShards(1).withSuffix(".csv"));

        p.run();
    }
}
