# Spark architecture:driver, executors, cluster mindset

# Driver = controls Spark application
# Executors = process distributed data
# Cluster mindset = data processed across multiple machines

from pyspark.sql import SparkSession

# SparkSession starts the Spark application
# Driver process gets created here

spark = SparkSession.builder \
    .appName("Spark Architecture Example") \
    .getOrCreate()

# Read clickstream dataset
events_df = spark.read.csv(
    "data/clickstream_events.csv",
    header=True,
    inferSchema=True
)

# Action
# Executors process partitions and return results
events_df.show()

spark.stop()