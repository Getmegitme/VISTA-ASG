#Reading and writing files: CSV, JSON, and Parquet

# Read CSV
# Write Parquet
# Read Parquet

from pyspark.sql import SparkSession

# Start Spark Session

spark = SparkSession.builder \
    .appName("CSV JSON Parquet Example") \
    .getOrCreate()

# Read CSV
events_df = spark.read.csv(
    "data/events.csv",
    header=True,
    inferSchema=True
)

print("=== CSV Schema ===")

df_csv.printSchema()

print("=== CSV Data ===")

df_csv.show()

# Write parquet
selected_df = df_csv.select(
    "user_id",
    "event_type",
    "country"
)

selected_df.write.mode("overwrite") \
    .parquet("output/events_parquet")
    
------------------------------------------

# Read parquet
df_parquet = spark.read.parquet(
    "output/events_parquet"
)

print("=== Parquet Data ===")

df_parquet.show()

# Parquet is columnar format.

# Spark reads only required columns, making analytics faster.

---------------
#•	Read the Parquet file back and compare it with the original CSV using count() to verify.
csv_count = selected_df.count()

parquet_count = df_parquet.count()

print("CSV Count:", csv_count)

print("Parquet Count:", parquet_count)

# Matching counts confirm that the data was written correctly.
----------------------

#•	Write the events Parquet file partitioned by event_date and explain why this would help a query that filters by date.

df_csv.write.mode("overwrite") \
    .partitionBy("event_date") \
    .parquet("output/events_partitioned")
    
# Data is split into folders by event_date.

# Queries filtering by date will scan only matching folders, improving performance.
