import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.jdbc.JdbcIO;
import org.apache.beam.sdk.io.kafka.KafkaIO;
import org.apache.beam.sdk.transforms.Count;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.transforms.Values;
import org.apache.beam.sdk.transforms.windowing.FixedWindows;
import org.apache.beam.sdk.transforms.windowing.Window;
import org.apache.beam.sdk.values.KV;
import org.apache.kafka.common.serialization.LongDeserializer;
import org.joda.time.Duration;

import java.sql.PreparedStatement;

public class RealTimeStreamingETL {
    public static void main(String[] args) {
        Pipeline p = Pipeline.create();

        p.apply(KafkaIO.<Long,IotEvent>read().withBootstrapServers("localhost:9092")
                .withTopic("beamtopic")
                .withKeyDeserializer(LongDeserializer.class)
                .withValueDeserializer(IotDeserializer.class)
                .withoutMetadata()
        )
                .apply(Values.<IotEvent>create())
                // We want to count an unbounded data, but this can not be performed using
                // Group by key except we use a fixed window.
                .apply(Window.<IotEvent>into(FixedWindows.of(Duration.standardSeconds(10))))
                // Count number of elements that has temperature > 80.0
                .apply(ParDo.of(new DoFn<IotEvent, String>() {
                    @ProcessElement
                    public void processElement(ProcessContext c){
                        if(c.element().getTemperature()>80.0){
                            c.output(c.element().getDeviceId());
                        }
                    }
                }))
                .apply(Count.perElement())
                .apply(JdbcIO.<KV<String,Long>>write().withDataSourceConfiguration(JdbcIO.DataSourceConfiguration
                        .create("com.mysql.jdbc.Driver", "jdbc:mysql://your_ip:3306/beamdb?useSSL=false")
                                .withUsername("root").withPassword("root"))
                        .withStatement("insert into event values (?,?) ")
                        .withPreparedStatementSetter(new JdbcIO.PreparedStatementSetter<KV<String,Long>>() {
                            @Override
                            public void setParameters(KV<String, Long> element, PreparedStatement preparedStatement) throws Exception {
                                preparedStatement.setString(1, element.getKey());
                                preparedStatement.setLong(2, element.getValue());
                            }
                        }));
/*                .apply(ParDo.of(new DoFn<KV<String,Long>, Void>() {

                    @ProcessElement
                    public void processElement(ProcessContext c){
                        System.out.println(c.element());

                    }
                }));*/
/*
                Print every device id in kafka message:
                .apply(ParDo.of(new DoFn<IotEvent, Void>() {

                    @ProcessElement
                    public void processElement(ProcessContext c){
                        System.out.println(c.element().getDeviceId());

                    }
                }));
*/



        p.run();

    }
}
