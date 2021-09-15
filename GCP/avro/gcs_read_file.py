import logging
import os
from google.cloud import storage as gcs
'''
    Read a file from GCS and print content.
'''

# Set bucket name to use
bucket_name = 'bucketoutputltc'

# Create GCS client manager.
storage_client = gcs.Client()
# Get the bucket from GCS
storage_client.get_bucket('bucket_name')

#[START read]
def read_file(filename):
    '''
    Print content of file in GCS
    :param filename:
    :return: None
    '''
    print('Reading the full file contents:\n')
    gcs_file = gcs.open(filename)
    contents = gcs_file.read()
    gcs_file.close()
    print(contents)
#[END read]

read_file(filename='fileName')
