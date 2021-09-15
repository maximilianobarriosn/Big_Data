import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.io.hdfs.HadoopFileSystemOptions;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.apache.hadoop.conf.Configuration;

import java.util.Collections;

public class HDFSExample {
    public static void main(String[] args) {

        // Connection between HDFS and apache beam
        Configuration conf = new Configuration();

        conf.set("fs.defaultFS", "hdfs://172.31.17.138:8020");
        conf.set("fs.hdfs.impl", org.apache.hadoop.hdfs.DistributedFileSystem.class.getName());
        conf.set("fs.file.impl", org.apache.hadoop.fs.LocalFileSystem.class.getName());

        String[] args1 = new String[] { "--hdfsConfiguration=[{\"fs.default.name\" : \"hdfs://172.31.17.138:8020\"}]",
                "--runner=DirectRunner" };

        HadoopFileSystemOptions hdfsOptions = PipelineOptionsFactory.fromArgs(args1)
                .withValidation().as(HadoopFileSystemOptions.class);

        hdfsOptions.setHdfsConfiguration(Collections.singletonList(conf));

        Pipeline p = Pipeline.create(hdfsOptions);

        PCollection<String> pHdfs = p.apply(TextIO.read().from("hdfs://172.31.17.138:8020/user/user.csv"));

        pHdfs.apply(ParDo.of(new DoFn<String, Void>() {

            @ProcessElement
            public void processElement(ProcessContext c){
                System.out.println(c.element());
            }
        }));
        }
}
