# Week 5 Mini Project
# Streaming Media Company...

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType
)

from pyspark.sql import functions as F

# Start Spark Session
---------------------------------------------------

spark = SparkSession.builder \
    .appName("Week5 Mini Project") \
    .getOrCreate()

# Define Explicit Schema
------------------------------------------------

schema = StructType([

    StructField(
        "event_id",
        IntegerType(),
        True
    ),

    StructField(
        "user_id",
        StringType(),
        True
    ),

    StructField(
        "event_type",
        StringType(),
        True
    ),

    StructField(
        "device",
        StringType(),
        True
    ),

    StructField(
        "country",
        StringType(),
        True
    ),

    StructField(
        "event_date",
        StringType(),
        True
    ),

    StructField(
        "session_time_sec",
        IntegerType(),
        True
    )

])

# Read Events CSV
---------------------------------------------------

events_df = spark.read.csv(
    "data/events.csv",
    header=True,
    schema=schema
)

# Read Users CSV
---------------------------------------------

users_df = spark.read.csv(
    "data/users.csv",
    header=True,
    inferSchema=True
)

# Check NULL Values
----------------------------------------------

null_user_count = events_df.filter(
    F.col("user_id").isNull()
).count()

null_event_type_count = events_df.filter(
    F.col("event_type").isNull()
).count()

print("NULL user_id rows:",
      null_user_count)

print("NULL event_type rows:",
      null_event_type_count)

# Separate Bad Records
--------------------------------------------------

bad_records_df = events_df.filter(
    F.col("event_id").isNull() |
    F.col("event_type").isNull()
)

print("=== Bad Records ===")

bad_records_df.show()

# Keep Valid Records
-------------------------------------------------

valid_df = events_df.filter(
    F.col("event_id").isNotNull() &
    F.col("event_type").isNotNull()
)

# Fill NULL user_id
-------------------------------------------------

valid_df = valid_df.fillna({
    "user_id": "anonymous"
})

# Join with Users Data
--------------------------------------------------

joined_df = valid_df.join(
    users_df,
    on="user_id",
    how="left"
)

# Add session_minutes Column
--------------------------------------------------

joined_df = joined_df.withColumn(
    "session_minutes",
    F.col("session_time_sec") / 60
)

# Aggregate Daily User Activity
--------------------------------------------------

summary_df = joined_df.groupBy(
    "user_id",
    "country",
    "event_date"
).agg(

    F.count("event_id").alias(
        "event_count"
    ),

    F.sum("session_minutes").alias(
        "total_session_minutes"
    ),

    F.collect_set("device").alias(
        "device_types"
    )

)

# Show Final Output
--------------------------------------------------

print("=== Daily User Activity Summary ===")

summary_df.show()

# Cache Data
--------------------------------------------------

summary_df.cache()

summary_df.count()

# Write Curated Output as Parquet
-------------------------------------------------

summary_df.write.mode("overwrite") \
    .partitionBy("event_date") \
    .parquet(
        "output/user_activity_summary"
    )

# Write Bad Records Separately
--------------------------------------------------

bad_records_df.write.mode("overwrite") \
    .parquet(
        "output/bad_records"
    )

# Stop Spark
--------------------------------------------------

spark.stop()