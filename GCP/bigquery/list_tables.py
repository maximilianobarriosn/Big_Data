from google.cloud import bigquery
client = bigquery.Client()
datasets = list(client.list_datasets())  # Make an API request.
project = client.project

if datasets:
    print("Datasets in project {}:".format(project))
    for dataset in datasets:
        print("\t{}".format(dataset.dataset_id))
        tables = client.list_tables(dataset.dataset_id)

        print("Tables contained in '{}':".format(dataset.dataset_id))
        for table in tables:
            print("{}.{}.{}".format(table.project, table.dataset_id, table.table_id))

else:
    print("{} project does not contain any datasets.".format(project))