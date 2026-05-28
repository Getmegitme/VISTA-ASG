--6. PythonOperator, BashOperator, and parameterization

##•	Write a PythonOperator task that reads context['ds'] and prints which date it is processing.

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

## Here, we are using context['ds']. It gives us the execution date in YYYY-MM-DD format.
def process_shipment_file(**context):

    execution_date = context['ds']

    print(f"Processing shipment file for date: {execution_date}")

# DAG
with DAG(

    dag_id="pythonoperator_context_example",

    start_date=datetime(2024, 1, 1),

    schedule_interval="@daily",

    catchup=False

) as dag:

    process_task = PythonOperator(

        task_id="process_shipment_file",

        python_callable=process_shipment_file

    )
    
## For example, if the DAG runs for 2024-01-15, then the output will be shown as "Processing shipment file for date: 2024-01-15"
---------------------------------------------------------------------

##•	Write a BashOperator that runs python /scripts/transform.py --date {{ ds }}

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(

    dag_id="bashoperator_example",

    start_date=datetime(2024, 1, 1),

    schedule_interval="@daily",

    catchup=False

) as dag:

    transform_task = BashOperator(

        task_id="transform_shipments",

        bash_command="python /scripts/transform.py --date {{ ds }}"

    )
--------------------------------------------------------------------------

##•	Store a variable called WAREHOUSE_URL in Airflow and read it inside a PythonOperator task.

from airflow.models import Variable
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def read_warehouse_url():

    warehouse_url = Variable.get("WAREHOUSE_URL")

    print(f"Warehouse URL: {warehouse_url}")

# DAG

with DAG(

    dag_id="airflow_variable_example",

    start_date=datetime(2024, 1, 1),

    schedule_interval="@daily",

    catchup=False

) as dag:

    variable_task = PythonOperator(

        task_id="read_variable",

        python_callable=read_warehouse_url

    )
-----------------------------------------------------------------------

##•	Explain the difference between provide_context=True and defining **kwargs in the function signature.

--The older versions used 'provide_context=True' inorder to pass Airflow context into functions.

--Example:
    PythonOperator(
    provide_context=True
)

--in Airflow, **kwargs automatically receives the context. So the modern approach goes by 
    def my_task(**kwargs):
##here, it doesnt need to use 'provide_context=True'
