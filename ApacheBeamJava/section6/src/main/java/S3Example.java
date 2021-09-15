import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;

public class S3Example {
    public static void main(String[] args) {
        Options myOption = PipelineOptionsFactory.fromArgs(args).withValidation().as(Options.class);
        Pipeline p = Pipeline.create(myOption);

        AWSCredentials awsCredObject = new BasicAWSCredentials(myOption.getAWSAccessKey(), myOption.getAWSSecretKey());

        myOption.setAwsCredentialsProvider(new AWSStaticCredentialsProvider(awsCredObject));

        PCollection<String> pInput =  p.apply(TextIO.read().from("s3://your_aws_bucket/input/user_order.csv"));

        pInput.apply(ParDo.of(new DoFn<String, Void>() {

            @ProcessElement
            public void processElement(ProcessContext c){
                System.out.println(c.element());
            }
        }));

        p.run();
    }
}
