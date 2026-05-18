# Partitions, shuffle, and basic performance thinking

# Cache DataFrame
# Trigger shuffle
# Understand performance basics

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("Partitions Shuffle Performance") \
    .getOrCreate()

# Read Events CSV

df = spark.read.csv(
    "data/events.csv",
    header=True,
    inferSchema=True
    
---------------------    
#•	Read the events CSV and print the number of partitions.

print("=== Current Number of Partitions ===")

print(df.rdd.getNumPartitions())

# Meaning:
# Spark splits data into partitions.
# Different executors process different partitions in parallel.
-----------------
#•	Repartition to 4 partitions, then cache the result and run show() and count() to confirm caching works.

df_repartitioned = df.repartition(4)

print("=== Partitions After Repartition ===")

print(df_repartitioned.rdd.getNumPartitions())

# Meaning: repartition(4)
# redistributes data into 4 partitions.
# Useful before joins or aggregations.
-----

#•	Explain in one sentence why groupBy causes a shuffle.

# Because, Spark must move rows with same group key to the same executor.
----------------------------------

#•	Explain when you would cache a DataFrame in a real pipeline.

# Cache is useful when same DataFrame is reused multiple times.