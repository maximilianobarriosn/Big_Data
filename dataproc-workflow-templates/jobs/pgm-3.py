from google.cloud import bigquery
from google.cloud import datacatalog_v1
from google.cloud.datacatalog_v1beta1 import PolicyTagManagerClient, types
from googleapiclient import discovery
from pyspark.sql import SparkSession
spark = SparkSession.builder.master('yarn').appName('spark-cloudsql').getOrCreate()
import io
import json
import sys

bq_client = bigquery.Client()

#############################################################################
### Get BigQuery Table Schema ###############################################
#############################################################################

fully_qualified_table_name = sys.argv[1]
project_id, dataset_id, table_id = fully_qualified_table_name.split(".")

dataset_ref = bq_client.dataset(dataset_id, project=project_id)
table_ref = dataset_ref.table(table_id)
table = bq_client.get_table(table_ref)

f = io.StringIO("")
bq_client.schema_to_json(table.schema, f)
bq_schema_json = json.loads(f.getvalue())

#############################################################################
### Get Cloud SQL Metadata for the BQ table #################################
#############################################################################

jdbc_url = "jdbc:postgresql://localhost:5432/postgres?user=postgres&password=root"

jdbc_properties = dict(
    user="postgres",
    password="root",
    driver="org.postgresql.Driver"
)

df = spark.read.jdbc(url=jdbc_url, table="public.metadata", properties=jdbc_properties)

df_rows_list = df.collect()

list_keys = []
list_values = []
metadata_dictionary = []
for row in df_rows_list:
    key = 'column_name'
    value = row['column_name']
    list_keys.append(key)
    list_values.append(value)
    for element in row['description'].split(";"):
        key, value = element.split("=")
        list_keys.append(key)
        list_values.append(value)
    dictionary = dict(zip(list_keys,list_values))
    metadata_dictionary.append(dictionary)

print(metadata_dictionary)

#############################################################################
### Data Catalog ############################################################
#############################################################################

update_flag = False
client = PolicyTagManagerClient()

taxonomy_parent = sys.argv[2]
taxonomy_to_search = sys.argv[3]
taxonomy_instance = ""
taxonomy_list = client.list_taxonomies(parent=taxonomy_parent)

for taxonomy in taxonomy_list:
    if (taxonomy.display_name == taxonomy_to_search):
        taxonomy_instance = taxonomy

    if not taxonomy_instance:
        print("Taxonomy specified does not exist")
    else:
        print(taxonomy_instance.name)

policy_tags_list = client.list_policy_tags(parent=taxonomy_instance.name)

for element_metadata in metadata_dictionary:
    policy_tag_instance = ""    
    for policy_tag in policy_tags_list:
        if (policy_tag.display_name == element_metadata['CON']):
            policy_tag_instance = policy_tag

        if not policy_tag_instance:
            print("Policy Tag specified does not exist")
        else:
            print(policy_tag_instance.name)

    for element_bq in bq_schema_json:
        if element_metadata['column_name'] == element_bq['name']:
            if not policy_tag_instance:
                if not (element_metadata['CON'] == 'Public' or element_metadata['CON'] == 'Internal Use'):
                    print("ERROR")
            else:
                try:
                    if element_bq['policyTags']:
                        if policy_tag_instance.name not in str(element_bq['policyTags']):
                            element_bq['policyTags'] = {'names': [policy_tag_instance.name]}
                            update_flag = True
                except:
                    element_bq['policyTags'] = {'names': [policy_tag_instance.name]}
                    update_flag = True

        print("Flag: " + str(update_flag))

print(bq_schema_json)

bigquery_api = discovery.build('bigquery', 'v2')

tables = bigquery_api.tables()
bq_schema_json = {'schema': {'fields': bq_schema_json}}

if update_flag:
    tables.patch(projectId=project_id, datasetId=dataset_id, tableId=table_id, body=bq_schema_json).execute()
else:
    print("No´policy tags to update in the table schema. Everything is up to date.")