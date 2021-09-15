import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.values.PCollection;

public class LocalFileExample {
    public static void main(String[] args) {

        Myoptions options = PipelineOptionsFactory.fromArgs(args).withValidation().as(Myoptions.class);


        Pipeline pipeline = Pipeline.create();
        String file_input_path = "/home/maximiliano.barrios/Documents/sections/section2/local_column_file.csv";
        String file_output_path = "/home/maximiliano.barrios/Documents/sections/section2/output.csv";

        PCollection<String> output = pipeline.apply(TextIO.read().from(options.getInputFile()));
        output.apply(TextIO.write().to(options.getOutputFile()).withNumShards(1).withSuffix(options.getExtn()));

        pipeline.run();
    }
}
