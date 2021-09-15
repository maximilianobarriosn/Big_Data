#!/usr/bin/env python
# coding: utf-8

# In[3]:


import findspark
findspark.init()
findspark.find()
import pyspark
findspark.find()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col,sum,avg,max
import pyspark.sql.functions as F
from pyspark.sql.types import BooleanType
from pyspark.sql.functions import split, explode

conf = pyspark.SparkConf().setAppName('appName').setMaster('local')
#sc = pyspark.SparkContext(conf=conf)
sc = SparkContext.getOrCreate()
spark = SparkSession(sc)
csv_df = spark.read.option("header", "True").csv("./web.csv")
csv_df.printSchema()


# In[136]:


csv_df.registerTempTable("df")

# Print complete table
spark.sql("SELECT * from df").show()

# Only process URL and Status from table, discarding result code != 200
only_200_result = spark.sql("SELECT URL, Staus from df WHERE Staus!=200")

# Print result of query
#spark.sql("SELECT URL, Staus from df WHERE Staus!=200").show()

# Split command from path

split_URL = pyspark.sql.functions.split(only_200_result['URL'], ' ')
url_df = only_200_result.withColumn('URL_COMMAND', split_URL.getItem(1))

# Register new table to spark sql query
url_df.registerTempTable("URL_Table")

# Obtain list of 10 paths and counts in desc order.
top_ten_200_result = spark.sql("SELECT Staus, URL_COMMAND from URL_Table")                                .groupBy("URL_COMMAND")                                .count().                                orderBy(col("count").desc())                                .take(10)

# Print result of query
spark.sql("SELECT Staus, URL_COMMAND from URL_Table")                                .groupBy("URL_COMMAND")                                .count().                                orderBy(col("count").desc()).show(10)

print("********************************************************")
print("Top 10 visited paths:")
print("********************************************************")

# Print elements of the list
for i in top_ten_200_result:
    print(i)


# In[64]:


ip_df = spark.sql("SELECT DISTINCT IP from df")
import ipaddress

@F.udf(returnType=BooleanType())
def is_ip(param_ip):
    try:
        ipaddress.ip_address(param_ip)
        return True
    except:
        return False
        
print("********************************************************")
print("Unique hosts:")
print("********************************************************")
ip_df.where(is_ip(col("IP"))==True).show()


# In[105]:


hosts_time= spark.sql("SELECT IP, Time from df")
# Split command from path
from pyspark.sql.functions import regexp_replace

# Split Time column by /
host_time_splitted = pyspark.sql.functions.split(hosts_time['Time'], '/')

# Get Day and Month columns
host_days = hosts_time.withColumn('Day', host_time_splitted.getItem(0)).withColumn('Month', host_time_splitted.getItem(1))

# Replace [ character by nothing
host_days = host_days.withColumn('Day', regexp_replace(col('Day'), "\\[", ""))

# Drop time column (not useful)
host_days = host_days.drop('Time')

# Drop invalid IP hosts
host_days = host_days.where(is_ip(col("IP"))==True)

# Group by Day and Month for different hosts
host_days = host_days.groupBy("Day", "Month").agg(F.countDistinct('IP'))

# Order by months
host_days = host_days.orderBy("Month")


print("********************************************************")
print("Number of access by different hosts per day/month:")
print("********************************************************")
# Show result from query
host_days.show()


# In[108]:


responses_304 = spark.sql("SELECT count(*) as 304_Responses_Count from df WHERE Staus=304")
responses_304.show()

print("********************************************************")
print("Number of 304 responses:")
print("********************************************************")


# In[135]:


# Print complete table
spark.sql("SELECT * from df").show()

# Only process URL and Status from table, discarding result code != 200
only_304_result = spark.sql("SELECT URL, Staus from df WHERE Staus==304")

# Print result of query
#spark.sql("SELECT URL, Staus from df WHERE Staus==304").show()

# Split command from path

split_URL = pyspark.sql.functions.split(only_304_result['URL'], ' ')
url_df = only_304_result.withColumn('URL_COMMAND', split_URL.getItem(1))

# Register new table to spark sql query
url_df.registerTempTable("URL_Table")

# Obtain list of 10 paths and counts in desc order.
top_five_304_result = spark.sql("SELECT Staus, URL_COMMAND from URL_Table")                                .groupBy("URL_COMMAND")                                .count().                                orderBy(col("count").desc())                                .take(10)

print("********************************************************")
print("Top five requested paths :")
print("********************************************************")
# Print result of query
spark.sql("SELECT Staus, URL_COMMAND from URL_Table")                                .groupBy("URL_COMMAND")                                .count().                                orderBy(col("count").desc()).show(5)


# In[134]:


# Print complete table
spark.sql("SELECT * from df").show()

# Only process URL and Status from table, discarding result code == 304
only_304_result = spark.sql("SELECT IP, Staus from df WHERE Staus==304")

# Print result of query
#spark.sql("SELECT IP, Staus from df WHERE Staus==304").show()


# Register new table to spark sql query
only_304_result.registerTempTable("IP_CODE_Table")

# Obtain list of 10 paths and counts in desc order.
top_five_304_result = spark.sql("SELECT * from IP_CODE_Table")                                .groupBy("IP")                                .count().                                orderBy(col("count").desc())                                .take(5)

print("********************************************************")
print("Top five hosts with 304 response :")
print("********************************************************")
# Print result of query
spark.sql("SELECT * from IP_CODE_Table")                                .groupBy("IP")                                .count().                                orderBy(col("count").desc()).show(5)


# In[133]:


# Print complete table
spark.sql("SELECT * from df").show()

# Only process URL and Status from table, discarding result code != 200
only_two_codes_result = spark.sql("SELECT Time, Staus from df WHERE Staus==206 OR Staus==404")

# Print result of query
#spark.sql("SELECT Time, Staus from df WHERE Staus==206 OR Staus==404").show()

# Split Time column by /
splitted_time = pyspark.sql.functions.split(only_two_codes_result['Time'], '/')

# Get Day and Month columns
only_two_codes_result = only_two_codes_result.withColumn('Day', splitted_time.getItem(0)).withColumn('Month', splitted_time.getItem(1))

only_two_codes_result = only_two_codes_result.drop('Time')

# Replace [ character by nothing
only_two_codes_result = only_two_codes_result.withColumn('Day', regexp_replace(col('Day'), "\\[", ""))

# Group by Day and Month for different hosts
only_two_codes_result = only_two_codes_result.groupBy("Day", "Month", "Staus").count()

only_two_codes_result = only_two_codes_result.orderBy("Month")

print("********************************************************")
print("Day/Month with 206/404 responses :")
print("********************************************************")
only_two_codes_result.show(1000)


# In[142]:


# Print complete table
spark.sql("SELECT * from df").show()

# Only process Time and Status from table with result code == 206 or 404
only_two_codes_by_hour_result = spark.sql("SELECT Time, Staus from df WHERE Staus==206 OR Staus==404")

# Print result of query
#spark.sql("SELECT Time, Staus from df WHERE Staus==206 OR Staus==404").show()

# Split Time column by /
splitted_time = pyspark.sql.functions.split(only_two_codes_by_hour_result['Time'], ':')

# Get Hour from Time Column
only_two_codes_by_hour_result = only_two_codes_by_hour_result.withColumn('Hour', splitted_time.getItem(1))

# Drop Time Column (not useful)
only_two_codes_by_hour_result = only_two_codes_by_hour_result.drop('Time')

# Group by Hour and Status
only_two_codes_by_hour_result = only_two_codes_by_hour_result.groupBy("Hour", "Staus").count()

# Order by Hour
only_two_codes_by_hour_result = only_two_codes_by_hour_result.orderBy("Hour")

print("********************************************************")
print("Hours with 206/404 responses :")
print("********************************************************")
only_two_codes_by_hour_result.show(1000)


# In[ ]:




