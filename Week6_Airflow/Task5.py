--5. Dependencies and dependency design
-----------------------------------------------------------------------------------
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

##•	Draw and implement a DAG where file_check runs first, then row_validation and schema_validation run in parallel, then load_warehouse runs after both validations succeed.

## TASK 1 - FILE CHECK
def file_check():

    print("Checking if shipment file exists")

    print("Shipment file found")
    
## TASK 2 - ROW VALIDATION
def row_validation():

    print("Validating shipment row counts")

    print("Checking duplicate records")

    print("Row validation successful")

## TASK 3 - SCHEMA VALIDATION
def schema_validation():

    print("Validating shipment schema")

    print("Checking required columns")

    print("Schema validation successful")

## TASK 4 - LOAD WAREHOUSE
##Here, we cleaned the shipment data
def load_warehouse():

    print("Loading shipment data into warehouse")

    print("Warehouse load completed")

## AIRFLOW DAG
## with 'DAG(' Starts Airflow pipeline.
## The schedule_interval is daily at 2:00 AM

with DAG(

    dag_id="logistics_dependency_pipeline",

    start_date=datetime(2024, 1, 1),

    schedule_interval="0 2 * * *",

    catchup=False

) as dag:

## Now, we will do the ROW VALIDATION TASK
row_validation_task = PythonOperator(

        task_id="row_validation",

        python_callable=row_validation

    )
    
## Now, the SCHEMA VALIDATION TASK
schema_validation_task = PythonOperator(

        task_id="schema_validation",

        python_callable=schema_validation

    )
    
## Now, we are LOADING TASK
    load_warehouse_task = PythonOperator(

        task_id="load_warehouse",

        python_callable=load_warehouse

    )

##The following is the Dependency design.
    file_check_task >> [

        row_validation_task,

        schema_validation_task

    ] >> load_warehouse_task
------------------------------------------------------------

##•	Explain what happens if transform_region_2 fails but transform_region_1 succeeds — does load_warehouse run?

--Let us suppose,

transform_region_1 = success
transform_region_2 = failed

--then, load_warehouse will NOT run

--because the Airflow is waiting for All Upstream tasks to succeed. 
--SO, one failed dependency will block the downstream execution.

-------------------------------------------------------------------------

##•	Convert a >> b >> c into explicit set_downstream calls.

##Here, we are using >> operator
##Given
a >> b >> c

##Equivalent explicit version

a.set_downstream(b)

b.set_downstream(c)

##Here, both of them will give same dependency behaviour
--------------------------------------------------------------------------

##•	Explain why circular dependencies are not allowed in a DAG.

## In DAG, no loops are allowed. Tasks would depend on themselves forever.
## In this way, we end up creating infinite execution loops. 
## Airflow, only allows one direction task flows.
