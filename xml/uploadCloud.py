from google.cloud import storage
import json

# credentials to get access google cloud storage
# write your key path in place of gcloud_private_key.json
storage_client = storage.Client.from_service_account_json('gcloud_private_key.json')

# write your bucket name in place of bucket1go
bucket_name = 'bucket1go'
BUCKET = storage_client.get_bucket(bucket_name)

def get_json(filename):
    '''
    this function will get the json object from
    google cloud storage bucket
    '''
    # get the blob
    blob = BUCKET.get_blob(filename)
    # load blob using json
    file_data = json.loads(blob.download_as_string())
    return file_data

# write the filename which you want
filename = 'albums.json'

# run the function and pass the filename which you want to get
get_json(filename)