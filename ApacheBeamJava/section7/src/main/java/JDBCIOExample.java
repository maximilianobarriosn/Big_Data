import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.coders.StringUtf8Coder;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.io.jdbc.JdbcIO;
import org.apache.beam.sdk.values.PCollection;

import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class JDBCIOExample {
    public static void main(String[] args) {
        Pipeline p = Pipeline.create();

        PCollection<String> pOutput = p.apply(JdbcIO.<String>read()
                .withDataSourceConfiguration(JdbcIO.DataSourceConfiguration
                .create("com.mysql.jdbc.Driver","jdbc:mysql://127.0.0.1:3306/products?useSSL=false")
                .withUsername("root").
                withPassword("root"))
                .withQuery("SELECT name, city, currency FROM product_info WHERE name = ? ")
                .withCoder(StringUtf8Coder.of())
                .withStatementPreparator(new JdbcIO.StatementPreparator() {
                    @Override
                    public void setParameters(PreparedStatement preparedStatement) throws Exception {
                            preparedStatement.setString(1,"pc");
                    }
                })
                .withRowMapper(new JdbcIO.RowMapper<String>() {

                    @Override
                    public String mapRow(ResultSet resultSet) throws Exception {
                        return resultSet.getString(1)+","+resultSet.getString(2)+","+resultSet.getString(3);
                    }
                }));
        pOutput.apply(TextIO.write().to("./jdbc_output.csv").withNumShards(1).withSuffix(".csv"));

        p.run();
    }
}
