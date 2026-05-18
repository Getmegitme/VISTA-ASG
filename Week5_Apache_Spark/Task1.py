#Why distributed processing exists

#Explain in simple words why a local script fails on very large data.

#Local Python loads everything into one machine memory (RAM)

import csv

with open("data/events.csv") as f:

    rows = list(csv.DictReader(f))

#Print total rows
print("Total Rows Using Local Python:", len(rows))

#Meaning:
#All rows are loaded into one machine memory.
#
#Small files work fine. But if the file is 500 GB or more, one laptop may run out of memory.

----------------------------------------------------------------------------------------------------------
#Describe one real business scenario where Spark would be needed and one where Python alone is enough.
#Spark
#Netflix processing billions of user click events daily. One machine cannot process that much data. So, Spark distributes the workload across many machines.

#Python
#Small Excel or CSV reports with few thousand rows.

---------------------------------
#Explain what parallel processing means using an everyday example.

#One person carrying 1000 boxes takes a long time.

#50 people carrying boxes together finish much faster.

#Spark works similarly using many machines.

#Stop Spark
spark.stop()