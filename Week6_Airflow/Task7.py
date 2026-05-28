--7. Monitoring, logging, and operational health

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.email import send_email
from datetime import datetime

##•	Write an on_failure_callback that prints the failed task ID and execution date to the log.

def alert_on_failure(context):

    # get failed task id

    task_id = context['task_instance'].task_id

    # get execution date

    execution_date = context['ds']

    # print logs

    print(f"FAILED TASK: {task_id}")

    print(f"EXECUTION DATE: {execution_date}")
------------------------------------------------------------------
##•	Configure a DAG to send an email alert on failure to a support address.

--When a task fails, Airflow will send an email automatically to the support team.

from airflow import DAG

from datetime import datetime

with DAG(

    dag_id="shipment_monitoring_pipeline",

    start_date=datetime(2024, 1, 1),

    schedule_interval="@daily",

    catchup=False,

    default_args={

        # support email

        "email": ["data-support@company.com"],

        # send email on failure

        "email_on_failure": True,

        # disable retry emails

        "email_on_retry": False

    }

) as dag:

    pass
    
--If the task fails, then the support team will receive an email alert.

-----------------------------------------------------------------------------

##•	Navigate the Airflow UI and find the log for a specific failed task run. Identify the error line.

--Step1: We open the Airflow UI
--Step2: Here we open the required DAG.
##Ex: logistics_daily_pipeline
--Step3: Here, we will find the RED failed task
##RED colour means that the task has failed.
--Step4: Click on the failed task
--Step5: We open the Logs tab
--Step6: Now, we scroll near the bottom and Find the ERROR

##Example:
FileNotFoundError:
shipments/2024-01-15.csv not found

--This means that the shipment file missing

--------------------------------------------------------------------

##•	Explain the difference between an SLA miss and a task failure.

--An SLA miss and a task failure are not the same thing in Airflow.

--An SLA miss happens when the task or DAG takes longer than the expected business deadline to complete. The task may still complete successfully, but it finished too late.

-- Example: File not found, API timeout

--A task failure happens when a task crashes or encounters an error during execution.
-- Example: Pipeline starts at 2:00 AM
-- Business expects its completion before 6:00 AM
-- Pipeline finishes it by 7:00 AM
-- This is an SLA miss because the pipeline missed the agreed completion time, even though no task technically failed.
