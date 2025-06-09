from flask import Flask, request
import requests
from google.cloud import storage
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def fetch_and_store():
    api_url = os.environ.get("API_URL", "https://fake-json-api.mock.beeceptor.com/users")
    bucket_name = os.environ.get("BUCKET_NAME")

    if not bucket_name:
        return "Missing BUCKET_NAME environment variable", 500

    response = requests.get(api_url)
    if response.status_code != 200:
        return f"API Error: {response.status_code}", 500
    data = response.json()

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    filename = f"api_data_{datetime.utcnow().isoformat()}.json"
    blob = bucket.blob(filename)
    blob.upload_from_string(str(data), content_type='application/json')

    return f"Success: Stored {filename}", 200

if __name__ == '__main__':
    app.run(debug=True)