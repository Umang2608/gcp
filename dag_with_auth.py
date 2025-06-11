from airflow import models
from airflow.operators.python_operator import PythonOperator
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import requests
from datetime import datetime

def trigger_cloud_run(**kwargs):
    cloud_run_url = 'https://your-cloud-run-url.a.run.app'  # No trailing slash

    # Generate ID token for authenticated request
    target_audience = cloud_run_url
    token = id_token.fetch_id_token(Request(), target_audience)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(cloud_run_url, headers=headers)
    print(f"Response status: {response.status_code}")
    print(response.text)

    if response.status_code != 200:
        raise Exception("Cloud Run call failed")

default_args = {
    'start_date': datetime(2024, 1, 1),
}

with models.DAG(
    'secure_trigger_cloud_run',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    trigger = PythonOperator(
        task_id='trigger_secure_cloud_run',
        python_callable=trigger_cloud_run,
        provide_context=True,
    )
