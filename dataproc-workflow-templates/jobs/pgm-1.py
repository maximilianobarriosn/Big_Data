from pyspark import SparkConf, SparkContext
import sys
conf = (SparkConf()
        .setMaster("local")
        .setAppName("App1"))
sc = SparkContext(conf = conf)
rdd = sc.textFile(sys.argv[1])
rdd_split = rdd.map(lambda x: x.split(","))
rdd_wo_header = rdd_split.filter(lambda x: "Pclass" not in x)
rdd_class_survived = rdd_wo_header.map(lambda x: (x[2],x[1]))
titanic_class = str(sys.argv[2])
rdd_class_filtered = rdd_class_survived.filter(lambda x: titanic_class == x[0])
rdd_class_filtered_formatted = rdd_class_filtered.map(lambda x: str(x[0]) + "," + str(x[1]))
rdd_class_filtered_formatted.coalesce(1,False).saveAsTextFile(sys.argv[3] + "/app1_result")