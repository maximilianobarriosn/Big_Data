#!/usr/bin/env python
# coding: utf-8

# In[25]:


import findspark
findspark.init()
findspark.find()
import pyspark
findspark.find()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col,sum,avg,max

conf = pyspark.SparkConf().setAppName('appName').setMaster('local')
#sc = pyspark.SparkContext(conf=conf)
spark = SparkSession(sc)
csv_df = spark.read.option("header", "True").csv("./web.csv")
csv_df.printSchema()
sc = SparkContext.getOrCreate();


# In[50]:


import pyspark.sql.functions as F
# Grouping respones by code
csv_df.groupBy('Staus').count().where(F.length("Staus")==3).show()


# In[70]:


from pyspark.sql.functions import col,sum,avg,max
from pyspark.sql.types import BooleanType
import ipaddress
@F.udf(returnType=BooleanType())
def is_ip(param_ip):
    try:
        ipaddress.ip_address(param_ip)
        return True
    except:
        return False
        
# Grouping by host IP and number of requests.
csv_df.groupBy('IP').count().where((col("count")>10) & (is_ip(col("IP"))==True)).show()


# In[106]:


from pyspark.sql.functions import split, explode
@F.udf(returnType=BooleanType())
def is_command(param_comm):
    try:
        if param_comm in ['POST', 'GET', 'HEAD']:
            return True
        else:
            return False
    except:
        return False

# Grouping by command and number of requests.
split_URL = pyspark.sql.functions.split(csv_df['URL'], ' ')
url_df = csv_df.withColumn('URL_COMMAND', split_URL.getItem(0)).groupBy('URL_COMMAND').count().where(is_command(col("URL_COMMAND"))).show(100)


# In[144]:


# Grouping by URI and number of requests    

# Drop unnecessary columns
filtered_URL_status = csv_df.drop('IP').drop('Time')

# Select by Status OK
filtered_200 = filtered_URL_status.where("Staus==200")

# Drop URL, adding URI column
URIs = filtered_200.withColumn('URI', split_URL.getItem(1)).drop('URL')

# Group by URI and count
total = URIs.groupBy("URI").count().orderBy(col("count").desc()).show(500)


# In[ ]:




