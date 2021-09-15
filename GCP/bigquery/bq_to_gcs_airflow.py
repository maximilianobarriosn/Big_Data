import csv
import datetime
import io
import logging

from airflow import models
import airflow.operators.dummy_operator as dummy
#from airflow.operators.d import dummy
from airflow.providers.google.cloud.transfers import bigquery_to_gcs
from airflow.providers.google.cloud.transfers import gcs_to_gcs
from google.cloud import bigquery
client = bigquery.Client(project='cdcproject-321019')

search_dataset = 'cdcproject'
dataset = client.get_dataset(search_dataset)  # Make an API request.
project = client.project

tables_list = []
def get_list_tables_from_dataset(project, dataset):
    if dataset:
        #print("Dataset in project {}:".format(project))
        #print("\t{}".format(dataset.dataset_id))
        tables = client.list_tables(dataset.dataset_id)

        #print("")
        #print("Tables contained in '{}':".format(dataset.dataset_id))
        for table in tables:
            tables_list.append(str(table.project) + '.' + str(table.dataset_id) + '.' + str(table.table_id))
            #print("{}.{}.{}".format(table.project, table.dataset_id, table.table_id))

    else:
        print("{} project does not contain any datasets.".format(project))

    return tables_list

list_of_tables = get_list_tables_from_dataset(project, dataset)
print(list_of_tables)

# --------------------------------------------------------------------------------
# Set default arguments
# --------------------------------------------------------------------------------

yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    'owner': 'airflow',
    'start_date': yesterday,
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=1),
}

# --------------------------------------------------------------------------------
# Set variables
# --------------------------------------------------------------------------------

# Destination Bucket
dest_bucket = 'us_dataset_copy'
source_bucket_gcs_to_gcs = 'us_dataset_copy'
dest_bucket_gcs_to_gcs = 'eu_dataset_copy'
# --------------------------------------------------------------------------------
# Set GCP logging
# --------------------------------------------------------------------------------

logger = logging.getLogger('bq_copy_to_eu_01')

# --------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Main DAG
# --------------------------------------------------------------------------------

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.
with models.DAG(
        'bq_copy_to_gcs',
        default_args=default_args,
        schedule_interval=None) as dag:
    start = dummy.DummyOperator(
        task_id='start',
        trigger_rule='all_success'
    )

    end = dummy.DummyOperator(
        task_id='end',
        trigger_rule='all_success'
    )


    # Loop over each record in the 'all_records' python list to build up
    # Airflow tasks
    for table in list_of_tables:
        logger.info('Generating tasks to transfer table: {}'.format(table))

        table_source = table

        BQ_to_GCS = bigquery_to_gcs.BigQueryToGCSOperator(
            # Replace ":" with valid character for Airflow task
            task_id='{}_BQ_to_GCS'.format(table_source.replace(":", "_")),
            source_project_dataset_table=table_source,
            destination_cloud_storage_uris=['{}-*.avro'.format(
                'gs://' + dest_bucket + '/' + table_source)],
            export_format='AVRO'
        )

        # Copy to a bucket in another location
        GCS_to_GCS = gcs_to_gcs.GCSToGCSOperator(
            # Replace ":" with valid character for Airflow task
            task_id='{}_GCS_to_GCS'.format(table_source.replace(":", "_")),
            source_bucket=source_bucket_gcs_to_gcs,
            source_object='{}-*.avro'.format(table_source),
            destination_bucket=dest_bucket_gcs_to_gcs,
            # destination_object='{}-*.avro'.format(table_dest)
        )

        start >> BQ_to_GCS >> GCS_to_GCS >> end