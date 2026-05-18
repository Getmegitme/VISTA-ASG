# Lazy evaluation and the transformation-action model

# Transformation examples:
# filter()
# select()

# Action examples:
# show()
# count()

# Lazy evaluation: Spark waits until action is called

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("Lazy Evaluation Example") \
    .getOrCreate()

# Read Dataset
---------------------------------------------------
df = spark.read.csv(
    "data/events.csv",
    header=True,
    inferSchema=True
)

# Transformation 1
---------------------------------------------
filtered_df = df.filter(
    F.col("country") == "India"
)

# Spark records the filter step
# but does NOT process data yet

# Transformation 2
------------------------------------------------
selected_df = filtered_df.select(
    "user_id",
    "event_type",
    "event_date"
)

# Spark records select step but still does NOT execute

# Transformation 3
------------------------------------------------
grouped_df = selected_df.groupBy(
    "event_type"
).count()

# Spark records aggregation plan but still NO execution happens

-----

#•	Add a show() at the end and explain what changes.
#
# Before show():
# Spark only stores execution plan.
#
# After show():
# Spark actually processes the data.
-------------------------------------------------------

#•	Explain why calling show() twice without caching may cause Spark to read and process the data twice.

# Spark may read and process the data again for each action. Without caching, same transformations rerun repeatedly.

----------------------------------------------

#•	Explain lazy evaluation using a cooking analogy.

# Spark watches us write recipe steps:
# - cut vegetables
# - boil water
# - add spices

# But cooking starts only when we say "serve food"
# show() and count() are like saying "serve food".
