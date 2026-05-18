#Core DataFrame operations: filter, select, join, and aggregate

# Filter rows
# Select columns
# Join DataFrames
# Aggregate data
# Add transformed columns

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("Core DataFrame Operations") \
    .getOrCreate()


# Read Events dataset
events_df = spark.read.csv(
    "data/events.csv",
    header=True,
    inferSchema=True
)

# Read users dataset
users_df = spark.read.csv(
    "data/users.csv",
    header=True,
    inferSchema=True
)

# Filter rows: Keep only purchase events

purchase_df = events_df.filter(
    F.col("event_type") == "purchase"
)

print("=== Purchase Events ===")

purchase_df.show()

# Practice Task:
# Count purchase events

purchase_count = purchase_df.count()

print("Purchase Event Count:", purchase_count)

# filter() works like SQL WHERE clause

# SELECT
# Choose required columns

selected_df = events_df.select(
    "user_id",
    "event_type",
    "event_date",
    "session_time_sec"
)

print("=== Selected Columns ===")

selected_df.show()

# select() reduces unnecessary columns and improves performance
--------------------------

# withColumn()
# Add session_minutes column
session_df = events_df.withColumn(
    "session_minutes",
    F.col("session_time_sec") / 60
)

print("=== Session Minutes Column ===")

session_df.show()

# withColumn() creates new columns or updates existing columns
-----------------------------

# JOIN
# Join events with users

joined_df = events_df.join(
    users_df,
    on="user_id",
    how="left"
)

print("=== Joined Data ===")

joined_df.show()

## Practice Task:
# Verify NULL user_id row

null_rows = joined_df.filter(
    F.col("user_name").isNull()
)

print("=== Rows With NULL user_name ===")

null_rows.show()

# Left join keeps all rows from events table.
# If no matching user exists, joined columns become NULL.

---------------------------------------------------
# GROUP BY + AGGREGATION

summary_df = events_df.groupBy(
    "country",
    "event_type"
).agg(
    F.count("event_id").alias("total_events"),
    F.sum("session_time_sec").alias("total_session_time")
)

print("=== Aggregated Summary ===")

summary_df.show()

# Meaning-
# groupBy() groups rows, agg() performs calculations
# count() = total rows, sum() = total session time

spark.stop()