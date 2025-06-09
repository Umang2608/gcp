from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Define your Cloud Run service URL
CLOUD_RUN_URL = "https://your-cloud-run-service-xyz.a.run.app/"

default_args = {
    'owner': 'data-engineer',
    'depends_on_past': False,
    'email': ['alerts@yourcompany.com'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='trigger_cloud_run_daily',
    default_args=default_args,
    description='Triggers a Cloud Run service daily from Cloud Composer',
    schedule_interval='0 7 * * *',  # every day at 7 AM UTC
    start_date=days_ago(1),
    catchup=False,
    tags=['cloud-run', 'composer'],
) as dag:

trigger_cloud_run = SimpleHttpOperator(
    task_id='invoke_cloud_run',
    http_conn_id=None,
    endpoint='https://your-cloud-run-service-xyz.a.run.app/',
    method='GET',
    headers={"Content-Type": "application/json"},
    dag=dag
)

