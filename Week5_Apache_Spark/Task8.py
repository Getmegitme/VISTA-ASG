# Schema definition and handling NULL values

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType
)

from pyspark.sql import functions as F

# Start Spark Session
--
spark = SparkSession.builder \
    .appName("Schema and NULL Handling") \
    .getOrCreate()
    
# Define Explicit Schema
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

# Meaning:
# StructType defines full schema.

# StructField defines:
# - column name
# - data type
# - NULL allowed or not
------------------------------------------

# Read CSV Using Schema

df = spark.read.csv(
    "data/events.csv",
    header=True,
    schema=schema
)
-----------------

#Practice tasks
#•	Load the events dataset with an explicit schema and run printSchema() to verify the types.
print("=== Schema ===")

df.printSchema()

# Meaning:
# Spark now uses provided schema instead of guessing data types

--------------

#•	Count how many rows have NULL user_id.

null_user_count = df.filter(
    F.col("user_id").isNull()
).count()

print("NULL user_id rows:", null_user_count)

# Meaning:
# isNull() identifies missing values.

---------------------------------------------------
# Check NULL event_type Rows

null_event_type_count = df.filter(
    F.col("event_type").isNull()
).count()

print("NULL event_type rows:", null_event_type_count)

---------------------

#•	Fill user_id NULLs with 'anonymous' and verify no NULLs remain in that column.
df_clean = df.fillna({
    "user_id": "anonymous",
    "session_time_sec": 0
})

print("=== Data After fillna ===")

df_clean.show()

# Meaning:
# fillna() replaces NULL values with default business values.
---------------------

# Verify NULL user_id Removed

remaining_null_user_count = df_clean.filter(
    F.col("user_id").isNull()
).count()

print("Remaining NULL user_id rows:",
      remaining_null_user_count)

---------------------------------------------------
# Drop Invalid Rows

df_valid = df_clean.dropna(
    subset=["event_id", "event_type"]
)

print("=== Valid Rows ===")

df_valid.show()

# Meaning:
# dropna() removes rows where important fields are NULL.
--------------------------------------------------------

spark.stop()

#•	Explain why inferSchema=True is risky in production when the source system changes a column type.

# Since Spark guesses data types automatically. It may infer wrong type, causing pipeline failures or incorrect aggregations.