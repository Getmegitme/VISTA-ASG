--Mini project: logistics company daily shipment pipeline

##•	A DAG named logistics_daily_pipeline scheduled to run at 2:00 AM daily.

--I created a DAG named:
    logistics_daily_pipeline
    
--The DAG is scheduled to run daily at:
    2:00 AM
    
--using the cron expression:
    schedule_interval='0 2 * * *'
    
--This will ensure that the shipment pipeline starts automatically every day without manual intervention.

##•	Task 1 — check_file_arrival: verify the shipment file exists for the execution date. Retry 5 times with a 20-minute delay to handle late arrivals.

--The task checks whether the shipment file exists for the current Airflow execution date.
    check_file_arrival
--The task will use 
    context['ds']
-- in order to dynamically generate the file path.

--Example:
    path = f'/data/shipments/{context["ds"]}.csv'
--The task was configured with:
    retries=5
    retry_delay=timedelta(minutes=20)
    
--This retry strategy handles late-arriving partner files without failing the pipeline immediately.

##•	Task 2 — validate_records: check row counts, required column presence, and NULL rates. Log results. Fail the task if critical columns have more than 5% NULLs.

validate_records

--The task performs data quality checks before transformation.

--Validation checks includes Row count validation, required column validation & NULL percentage checks
--The task logs total row counts, missing column details and NULL percentages

--Then we check the critical columns for the Values that are more than 5%.

--If the NULL value columns are exceeded, then we run 
    raise ValueError("Critical NULL threshold exceeded")
    
--This will prevent the poor-quality shipment data from entering downstream warehouse systems.

##•	Task 3 — transform_records: standardize column names, remove duplicates, and enrich with region codes using a lookup file.

--The 'transform_records' task standardizes and cleans shipment data before warehouse loading.

--Example
    df.columns = [col.lower() for col in df.columns]
--and 
    df = df.drop_duplicates()

-- We have also attached a lookup file ('region codes') to shipment records for downstream reporting and analytics.

##•	Task 4 — load_to_warehouse: load transformed records to the warehouse using an idempotent DELETE-then-INSERT pattern scoped to the execution date.

--The 'load_to_warehouse' task loads transformed shipment data into the warehouse.

--The task was designed using 'idempotent DELETE-then-INSERT'
--Example using SQL logic
    DELETE FROM shipments
    WHERE shipment_date = execution_date;
--For our code:
    INSERT INTO shipments
    SELECT *
    FROM transformed_shipments;
    
##•	All tasks must use context['ds'] to scope work to the correct date.

--All the tasks used ('context['ds']') inorder to process data for the current Airflow execution date.
--Example
    execution_date = context['ds']
    
--This value was used for file paths, warehouse deletes, inserts, logging and transformations
--This will allow reruns, retries and backfills to process the correct historical date automatically.

##•	Configure an on_failure_callback that logs the failed task name and execution date.

--An on_failure_callback was configured to capture task failures.
--The callback logs failed task ID, DAG name, execution date. 

--with the following example we can improve operational monitoring and debugging for suppoert engineers.

def on_failure(context):

    print(
        f"FAILED: {context['task_instance'].task_id}"
    )

    print(
        f"DATE: {context['ds']}"
    )

##•	Set an SLA of 4 hours on the DAG.

--The following DAG is configured with an SLA of 4 hours using 
    sla=timedelta(hours=4)
--Usually the DAG starts at 2 AM. The pipeline must be completed before 6 AM. 
--If the DAG exceeds this time, then 'SLA miss alerts are triggered' to notify the support team.

##•	Run a backfill for the past 3 days and verify correctness.

--I executed a backfill using the following code
    airflow dags backfill logistics_daily_pipeline \
    start-date 2024-01-01 \
    end-date 2024-01-03
    
--Airflow created separate DAG runs for Jan 1, Jan 2 and Jan 3
--Each run processed its own execution date using 'context['ds']'
--This shows that the Logs has confirmed correct processing for each historical date.

--------------------------------------------------------------------------------------------------
## Student deliverables
--------------------------------------------------------------------------------------------------
##•	A working DAG file that runs without errors in a local Airflow environment.

--The DAG file was placed inside 'airflow/dags/' and then the Airflow scheduler and webserver were started successfully.

--The DAG 'logistics_daily_pipeline' was visible in the Airflow UI and executed successfully without errors.
--So, all of the task dependencies, retries, callbacks, and SLA configurations worked correctly.

##•	A brief explanation of why each task was made idempotent and how.

--Each task was designed to be IDEMPOTENT. so rerunning tasks produces the same final result.

--check_file_arrival only checks file existence
--validate_records only validates and logs
--transform_records applies repeatable transformations
--load_to_warehouse uses DELETE-then-INSERT to avoid duplicates

--This protects the warehouse consistency, dashboard accuracy, retry safety.

##•	A screenshot or description of a failed task log from the Airflow UI.

--The 'check_file_arrival' task was intentionally failed using an invalid file path.
--The Airflow UI showed 
--task turning yellow during retries
--task turning red after retry exhaustion

--The log displayed 
    FileNotFoundError:
    Shipment file missing
    
--This will verify retry handling, log capture and the monitoring functionality successfully.

##•	An explanation of the retry strategy chosen for check_file_arrival.

--The shipment files sometimes arrive late from external partners.
--To handle this 'check_file_arrival' was configured with 

retries=5
retry_delay=timedelta(minutes=20)

--This allows the DAG to wait for delayed files, retry it automatically and reduce manual intervention

Total waiting time is 100 minutes before permanent failure. Since we are tryinng it 5 times with retries.

##•	An explanation of what happens if transform_records fails — which tasks are affected and why.

--If 'transform_records' fails, then 'load_to_warehouse' does not run.
--This is because of the dependency chain which is as follows
'validate_records - transform_records - load_to_warehouse'

--Airflow only triggers downstream tasks when all the upstream tasks succeed.
--This prevents incomplete data, corrupted warehouse loads and inaccurate reporting from reaching downstream systems.