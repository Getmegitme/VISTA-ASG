--2. Core Airflow concepts

from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

# TASK 1 - INGEST
def ingest_data():

    print("Ingesting shipment file")

# TASK 2 - VALIDATE
def validate_data():

    print("Validating shipment records")

# TASK 3 - REPORT
def generate_report():

   print("Generating shipment report")

---------------------------------------------------------------
#With DAG
with DAG(

    dag_id="shipment_midnight_pipeline",

    start_date=datetime(2024, 1, 1),

    schedule_interval="0 0 * * *",

    catchup=False

) as dag:

    ingest = PythonOperator(

        task_id="ingest_task",

        python_callable=ingest_data

    )

    validate = PythonOperator(

        task_id="validate_task",

        python_callable=validate_data

    )

    report = PythonOperator(

        task_id="report_task",

        python_callable=generate_report

    )

    ingest >> validate >> report
    
 ##•	Change the dependency so validate and ingest run in parallel and report only runs after both succeed.
 with DAG(

    dag_id="parallel_dependency_pipeline",

    start_date=datetime(2024, 1, 1),

    schedule_interval="@daily",

    catchup=False

) as dag:

    ingest = PythonOperator(

        task_id="ingest_task",

        python_callable=ingest_data

    )

    validate = PythonOperator(

        task_id="validate_task",

        python_callable=validate_data

    )

    report = PythonOperator(

        task_id="report_task",

        python_callable=generate_report

    )

    # Parallel dependency

    [ingest, validate] >> report
------------------------------------------------------------------
##3•	Explain what happens if catchup=True and start_date is set to 6 months ago.

start_date=datetime(2024,1,1)
catchup=True

## Here, let us consider today's date as July 2024 and given is to set 6 months ago. 
## Now, the Airflow will automatically create and run ALL the missed DAG runs from January until today.

-------------------------------------------------------------------
##4•	Explain what dag_id is and why it must be unique.

dag_id="logistics_daily_pipeline"

##dag_id is the unique name of the DAG in Airflow

## If two DAGs use the same dag_id, then Airflow gets confused and may overwrite metadata.
## So, every DAG must have a unique dag_id