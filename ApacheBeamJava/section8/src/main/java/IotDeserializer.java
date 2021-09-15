import org.apache.kafka.common.header.Headers;
import org.apache.kafka.common.serialization.Deserializer;
import org.codehaus.jackson.map.ObjectMapper;

import java.util.Map;

public class IotDeserializer implements Deserializer<IotEvent> {


    @Override
    public void configure(Map configs, boolean isKey) {
        Deserializer.super.configure(configs, isKey);
    }

    @Override
    public IotEvent deserialize(String s, byte[] bytes) {
        return null;
    }

    @Override
    public IotEvent deserialize(String topic, Headers headers, byte[] data) {
        ObjectMapper om = new ObjectMapper();
        IotEvent iotEvent = null;
        try{
            iotEvent = om.readValue(data, IotEvent.class);

        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return iotEvent;
    }

    @Override
    public void close() {
        Deserializer.super.close();
    }
}
