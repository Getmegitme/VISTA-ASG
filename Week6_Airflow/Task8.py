--8. Building the full logistics pipeline — end-to-end DAG

--•	Implement the full DAG above in your local Airflow environment and trigger it manually from the UI.

-- I implemented the full logistics pipeline DAG in the local Airflow environment using:

--PythonOperator
--retries
--retry delays
--SLA configuration
--failure callback
--task dependencies

-- The DAG flow is:
-- check_file_arrival - validate_records - transform_records - load_to_warehouse

-- I scheduled the DAG using 
schedule_interval='0 2 * * *'
-- Then after placed the DAG file inside: airflow/dags/

---------------------------------------------------------------

##•	Add a send_report task after load that runs in parallel with load (both triggered after transform).

-- Here, we want the Transform task to finish first and then in parallel we will load task runs and send_report task runs

def send_report(**context):

    date = context['ds']

    print(f"Sending shipment report for {date}")

send_report_task = PythonOperator(

    task_id='send_report',

    python_callable=send_report

)

transform >> [load, send_report_task]

--This means that after the transform succeeds, both the tasks start together.

-------------------------------------------------------------------------------------------------

##•	Force the file_check task to fail by pointing it to a non-existent file. Observe the retry behavior in the UI.

-- Lets use the incorrect file path to see that Airflow retries it automatically.

def check_file_arrival(**context):

    date = context['ds']

    # incorrect path

    path = f'/wrong_folder/{date}.csv'

    if not os.path.exists(path):

        raise FileNotFoundError(

            f'Shipment file missing: {path}'

        )

-- In Airflow, teh task will fail because the file does not exist. 
-- It will again retry the code with the function-
retries=5

retry_delay=timedelta(minutes=20)

--In the UI, we can see it as RED (Failed). If it is in YELLOW(It is retrying).
--In the Log, it will show as
--FileNotFoundError:
--Shipment file missing
---------------------------------------------------------------------------------------------

##•	Run a backfill for the past 3 days and verify that each run processes the correct date.

--I used the Airflow backfill command to rerun the DAG for historical dates.

airflow dags backfill logistics_daily_pipeline \
--start-date 2024-01-01 \
--end-date 2024-01-03

--Airflow created: one DAG run for each date - Jan 1, Jan 2 & Jan 3
--Each DAG run received its own execution date using: context['ds']

--Noe, the Logs will confirm the correct processing:
    Processing shipments for 2024-01-01
    Processing shipments for 2024-01-02
    Processing shipments for 2024-01-03
    
-- This will verify that each backfill run processed the correct historical execution date.

