--4. Idempotency 
---------------------------------------------------------------
##•	Explain why a plain INSERT without a DELETE is not idempotent.

INSERT INTO shipments
SELECT * FROM staging_shipments;

##A plain INSERT is not idempotent because every rerun inserts the same records again.
##If the task runs twice, then same shipment rows get inserted twice. It will create duplicat values and incorrect dashboards. 
##So, running a task multiple times will change the final output. \
##This shows that it is NOT Idempotent
-------------------------------------------------------------------------------------
##•	Rewrite a non-idempotent load function using the DELETE-then-INSERT pattern.

def load_to_warehouse(**context):

    execution_date = context['ds']

    print(f"""
    DELETE FROM shipments
    WHERE shipment_date = '{execution_date}'
    """)

    print(f"""
    INSERT INTO shipments
    SELECT *
    FROM staging_shipments
    WHERE shipment_date = '{execution_date}'
    """)
--------------------------------------------------
##•	Explain how context['ds'] works and write a function that uses it to scope a warehouse delete.

context['ds']

##It gives execution date of current Airflow run. Its format would be YYYY-MM-DD
##In our case, lets consider 2024-01-01
##For Example:

def delete_existing_shipments(**context):

    execution_date = context['ds']

    print(f"""
    DELETE FROM shipments
    WHERE shipment_date = '{execution_date}'
    """)
##If this DAG runs for '224-01-01', then query only deletes from shipments where shipment_date= '2024-01-01'
##This will delete only the records and not the whole table.

---------------------------------------------------------------
##•	Explain why writing Parquet with mode='overwrite' to a dated partition is idempotent.

df.write.mode("overwrite") \
.parquet(f"output/date={execution_date}")

##If suppose, 

execution_date = 2024-01-01

##Then,output path becomes,

output/date=2024-01-01

##If the task reruns, then same partition gets overwritten and old data is replaced with new data.

##Final data will remain same nad rerunning does not create any duplicates.

##WIth this, t makes it IDEMPOTENT.
