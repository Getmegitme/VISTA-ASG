-- 1. Why orchestration exists 

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# STEP 1
def ingest_file():

    print("Shipment file received successfully")

# STEP 2
def validate_file():

    print("Validation successful")

# STEP 3
def transform_records():

    print("Transformation successful")

# STEP 4
def load_warehouse():

    print("Warehouse load successful")

# AIRFLOW DAG
with DAG(

    dag_id="logistics_orchestration_pipeline",

    start_date=datetime(2024, 1, 1),

    schedule_interval="0 2 * * *",

    catchup=False,

    default_args={

        "retries": 3,

        "retry_delay": timedelta(minutes=5)

    }

) as dag:

    ingest_task = PythonOperator(

        task_id="ingest_file",

        python_callable=ingest_file

    )

    validate_task = PythonOperator(

        task_id="validate_file",

        python_callable=validate_file

    )

    transform_task = PythonOperator(

        task_id="transform_records",

        python_callable=transform_records

    )

    load_task = PythonOperator(

        task_id="load_warehouse",

        python_callable=load_warehouse

    )

# DEPENDENCY FLOW
    ingest_task >> validate_task >> transform_task >> load_task