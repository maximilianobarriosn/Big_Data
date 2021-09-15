import datetime

'''
    This app downloads an avro file from GCS and writes to a local file. Then
    converts it to json and returns in a http request using Flask.
     
    Directory must has: app.yaml, requirements.txt and main.py to run Flask App.
    
    Deploying the app - steps:
    
    gcloud auth login USER_ACCOUNT
    gcloud auth default
    gcloud config set project PROJECT_ID
    gcloud app create
    gcloud auth application-default login
    python3 -m venv env # create virtualenv 
    source env/bin/activate # activate virtualenv
    vim main.py # create app main
    vim requirements.txt # can use pip3 freeze > requirements.txt
    vim app.yaml # create app.yaml
    pip3 install -r requirements.txt
    gcloud app deploy
    gcloud app browse
'''

from flask import Flask, jsonify
from google.cloud import storage
app = Flask(__name__)

import os
import copy
import json
import avro
from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, DatumReader

try:
    # Delete local avro file if exist.
    print("Deleting avro file...")
    os.remove("fileavro.avro")
    print("Avro file deteled.")
except:
    pass

# Set bucket and filename to read from GCS
bucketname='bucketoutputltc'
filename='fileName'

# Create client manager in GCS
client = storage.Client()
bucket = client.bucket(bucketname)
blob = bucket.blob(filename)

# Write file from GCS to a local avro file.
with open('fileavro.avro', 'wb') as f:
    blob.download_to_file(f)

# Read data from avro file and convert to json
items2json = []
with open('fileavro.avro', 'rb') as f:
    reader = DataFileReader(f, DatumReader())
    metadata = copy.deepcopy(reader.meta)
    schema_from_file = json.loads(metadata['avro.schema'])
    items2json = [items for items in reader]
    reader.close()


@app.route('/')
def root():
    # Return json answer (avro -> json)
    return jsonify(items2json)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

