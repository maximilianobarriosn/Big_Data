from google.cloud import storage
import sys

bucket_name = sys.argv[1].replace("gs://","")
prefix = sys.argv[2]

print(bucket_name)
print(prefix)

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
blobs = bucket.list_blobs(prefix=prefix)

for blob in blobs:
    blob.delete()