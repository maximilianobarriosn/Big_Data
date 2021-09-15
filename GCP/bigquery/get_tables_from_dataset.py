from google.cloud import bigquery
client = bigquery.Client(project='your_project_id')

search_dataset = 'your_dataset'
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