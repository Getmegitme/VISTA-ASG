--3. Retries, backfills, SLAs, and task states

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# INGEST SHIPMENT FILE
def ingest_file():

    print("Shipment file received successfully")
    
# VALIDATE SHIPMENT FILE
def validate_shipment_file():

    print("Checking if shipment file exists")

    print("Validating shipment records")

    print("Validation successful")

# TRANSFORM RECORDS
def transform_records():

    print("Transforming shipment records")

    print("Removing duplicate rows")

    print("Transformation completed")

# LOAD WAREHOUSE
def load_warehouse():

    print("Loading records into warehouse")

    print("Warehouse load completed")
    
# AIRFLOW DAG
with DAG(

    dag_id="logistics_daily_pipeline",

    start_date=datetime(2024, 1, 1),

    schedule_interval="0 2 * * *",

    catchup=False,

    default_args={

        # default retry settings

        "retries": 3,

        "retry_delay": timedelta(minutes=10),

        # DAG must finish within 4 hours

        "sla": timedelta(hours=4)

    }

) as dag:

# INGEST TASK
ingest = PythonOperator(

        task_id="ingest_file",

        python_callable=ingest_file,

        retries=5,

        retry_delay=timedelta(minutes=20) )
        
# VALIDATE TASK
validate = PythonOperator(

        task_id="validate_file",

        python_callable=validate_shipment_file,

        retries=5,

        retry_delay=timedelta(minutes=15) )

# TRANSFORM TASK
transform = PythonOperator(

        task_id="transform_records",

        python_callable=transform_records,

        retries=2,

        retry_delay=timedelta(minutes=5) )
        
# LOAD TASK
load = PythonOperator(

        task_id="load_warehouse",

        python_callable=load_warehouse)
        
# DEPENDENCY CHAIN
    ingest >> validate >> transform >> load

------------------------------------------------------------------------

##Practice Tasks
##1•	Configure a DAG where the ingest task retries 5 times with a 20-minute delay and the transform task retries 2 times with a 5-minute delay.

ingest:
retries=5
retry_delay=20 minutes

transform:
retries=2
retry_delay=5 minutes

##2•	Set an SLA of 3 hours on the entire DAG and explain what happens if it is missed.

sla=timedelta(hours=3)

##Airflow will send the SLA miss alert if it is missed. It can send through Email, Slack or other ways.

##3•	Explain the difference between failed and upstream_failed task states.

##Failed - here the task is ran first, and then fails.
##upstream_failed - Here the task is never ran before. 

##4•	Run a backfill for the past 7 days from the Airflow CLI and explain what it does.

airflow dags backfill logistics_daily_pipeline \
--start-date 2024-01-01 \
--end-date 2024-01-07

This shows the rerun pipeline for old historical dates