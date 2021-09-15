import com.google.api.services.bigquery.model.TableFieldSchema;
import com.google.api.services.bigquery.model.TableRow;
import com.google.api.services.bigquery.model.TableSchema;

import java.util.Arrays;

class BigQuerySchema {
    public static TableSchema createSchema() {
        TableSchema schema =
                new TableSchema()
                        .setFields(
                                Arrays.asList(
                                        new TableFieldSchema()
                                                .setName("id")
                                                .setType("INT64")
                                                .setMode("REQUIRED"),
                                        new TableFieldSchema()
                                                .setName("name")
                                                .setType("STRING")
                                                .setMode("NULLABLE"),
                                        new TableFieldSchema()
                                                .setName("lastname")
                                                .setType("STRING")
                                                .setMode("NULLABLE")));
        return schema;
    }

}