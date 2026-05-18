# RDD vs DataFrame vs Spark SQL

#Topic: RDD, DataFrame, and Spark SQL
# RDD = low level distributed dataset
# DataFrame = structured distributed table
# Spark SQL = SQL queries on DataFrames

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("RDD vs DataFrame vs Spark SQL") \
    .getOrCreate()
    
# RDD Example
# RDD = low-level distributed dataset

rdd = spark.sparkContext.textFile(
    "data/events.csv"
)

print("=== RDD Count ===")

print(rdd.count())

# Meaning: RDD reads raw text lines.

# Spark does not automatically understand column names, schema, data types   
----------------------------------
# DataFrame Example

df = spark.read.csv(
    "data/events.csv",
    header=True,
    inferSchema=True
)
print("=== DataFrame First 5 Rows ===")

# Print first 5 rows
df.show(5)
-----------------------------------

# Count events by country using SQL

result = spark.sql("""

SELECT
    country,
    COUNT(*) AS event_count
FROM events
GROUP BY country

""")

print("=== Spark SQL Result ===")

result.show()
-----------------------------------------

# Explain in plain English why DataFrames are preferred over RDDs for most work today.

# DataFrames are easier to write, requires less code, and Spark automatically optimizes them.

# They are faster and simpler for most modern data engineering work.