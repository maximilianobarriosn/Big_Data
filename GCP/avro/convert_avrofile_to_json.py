import copy
import json
import avro
from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, DatumReader

'''
    Read data from an avro file and convert it to JSON
'''
with open('avro_file_example.avro', 'rb') as f:
    reader = DataFileReader(f, DatumReader())
    metadata = copy.deepcopy(reader.meta)
    schema_from_file = json.loads(metadata['avro.schema'])
    items2json = [items for items in reader]
    print(items2json)
    reader.close()

