import org.apache.avro.Schema;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.coders.AvroCoder;
import org.apache.beam.sdk.io.FileIO;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.io.parquet.ParquetIO;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.transforms.SimpleFunction;
import org.apache.beam.sdk.values.PCollection;

class BeamCustUtil {
    public static Schema getSchema(){

        String SCHEMA_STRING =
                "{\"namespace\": \"section6\",\n"
                        + " \"type\": \"record\",\n"
                        + " \"name\": \"ParquetExample\",\n"
                        + " \"fields\": [\n"
                        + "     {\"name\": \"SessionId\", \"type\": \"string\"},\n"
                        + "     {\"name\": \"UserId\", \"type\": \"string\"},\n"
                        + "     {\"name\": \"UserName\", \"type\": \"string\"},\n"
                        + "     {\"name\": \"VideoId\", \"type\": \"string\"},\n"
                        + "     {\"name\": \"Duration\", \"type\": \"string\"},\n"
                        + "     {\"name\": \"StartedTime\", \"type\": \"string\"},\n"
                        + "     {\"name\": \"Sex\", \"type\": \"string\"}\n"
                        + " ]\n"
                        + "}";
        Schema SCHEMA = new Schema.Parser().parse(SCHEMA_STRING);
        return SCHEMA;
    }
}

class ConvertCsvToGeneric extends SimpleFunction<String, GenericRecord>{

    @Override
    public GenericRecord apply(String input){

        String arr[] = input.split(",");

        Schema schema = BeamCustUtil.getSchema();
        GenericRecord record = new GenericData.Record(schema);

        record.put("SessionId", arr[0]);
        record.put("UserId", arr[1]);
        record.put("UserName", arr[2]);
        record.put("VideoId", arr[3]);
        record.put("Duration", arr[4]);

//        record.put("Duration", Integer.parseInt(arr[4]));
        record.put("StartedTime", arr[5]);
        record.put("Sex", arr[6]);

        return record;
    }
}
public class ParquetIOExample {
    public static void main(String[] args) {
        Pipeline p = Pipeline.create();

        Schema schema = BeamCustUtil.getSchema();

        PCollection<GenericRecord> pOutput = p.apply(TextIO.read().from("./user.csv"))
                                            .apply(MapElements.via(new ConvertCsvToGeneric()))
                                            .setCoder(AvroCoder.of(GenericRecord.class, schema));

/*        pOutput.apply(ParDo.of(new DoFn<GenericRecord, Void>() {

            @ProcessElement
            public void processElement(ProcessContext c){
                System.out.println(c.element());
            }
        }));*/

                pOutput.apply(FileIO.<GenericRecord>write().via(ParquetIO.sink(schema))
                .to("./parquetexample1")
                .withNumShards(1).withSuffix(".parquet"));

        p.run();
    }
}


