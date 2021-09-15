import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.parquet.ParquetIO;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.transforms.SimpleFunction;
import org.apache.beam.sdk.values.PCollection;

import java.beans.SimpleBeanInfo;

class PrintElem extends SimpleFunction<GenericRecord, Void>{

    @Override
    public Void apply(GenericRecord input){

        System.out.println(input.get("SessionId"));
        return null;
    }
}
public class ParquetIOWriteExample {
    public static void main(String[] args) {
        Pipeline p = Pipeline.create();
        Schema schema = BeamCustUtil.getSchema();

        PCollection<GenericRecord> pOuptut = p.apply(ParquetIO.read(schema).from("./file.parquet"));

        pOuptut.apply(MapElements.via(new PrintElem()));

        p.run();
    }
}
