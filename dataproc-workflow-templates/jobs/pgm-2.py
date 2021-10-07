from pyspark.sql import SparkSession
import sys
spark = SparkSession.builder.master('yarn').appName('spark-bigquery').getOrCreate()
bucket = sys.argv[1] + "/temp"
bucket = bucket.replace("gs://","")
spark.conf.set('temporaryGcsBucket', bucket)
survived = spark.read.format('csv').load(sys.argv[1] + "/app1_result/part*")
survived = survived.withColumnRenamed("_c0","Pclass")
survived = survived.withColumnRenamed("_c1","Survived")
survived.createOrReplaceTempView('titanic')
survived_total = spark.sql('SELECT CASE WHEN Survived = 0 THEN "No" ELSE "Yes" END AS survived, COUNT(Survived) AS total FROM titanic GROUP BY Survived ORDER BY total DESC')
survived_total = survived_total.withColumn("total", survived_total.total.cast('int'))
survived_total.show()
survived_total.write.format('bigquery').option('table', sys.argv[2]).mode("overwrite").save()
