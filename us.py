from flask import Flask, request
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
import os

app = Flask(__name__)

def run():
    project_id = "cpc-s-iquarshie-prj"
    bucket_name = "ikq_demo1"
    file_name = "products_data.json"
    dataset_id = "ikq_gcp_bq_testing"
    table_id = "products_table"

    uri = f"gs://{bucket_name}/{file_name}"
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    client = bigquery.Client(project=project_id)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
    )

    try:
        load_job = client.load_table_from_uri(
            source_uris=uri,
            destination=full_table_id,
            job_config=job_config
        )
        load_job.result()
        print(f"Loaded {file_name} from {bucket_name} into BigQuery table {full_table_id}")
    except GoogleAPIError as e:
        print("BigQuery API error:", e)
        if hasattr(e, 'errors'):
            print("Job errors:", e.errors)
    except Exception as e:
        print("Unexpected error:", e)

@app.route('/', methods=['POST'])
def trigger():
    run()
    return "Success", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
