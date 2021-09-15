from fastavro import reader, json_writer

'''
    Read an avro file and write to json file.
'''
with open("json_file_example.json", "w") as json_file:
    with open("avro_file_example.avro", "rb") as avro_file:
        avro_reader = reader(avro_file)
        json_writer(json_file, avro_reader.writer_schema, avro_reader)
