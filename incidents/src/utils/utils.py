from dotenv import load_dotenv
from google.cloud import storage
from os import environ


class CommonUtils():
    
    def upload_file_to_gcs_by_file(self, file_obj, destination_blob_name):
        
        load_dotenv('.env.template')         
        bucket_name = environ.get('BUCKET_NAME')
        
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name) 

        blob.upload_from_file(file_obj, content_type=file_obj.content_type)

    def upload_file_to_gcs_by_path(self, source_file_path, destination_blob_name):
        
        load_dotenv('.env.template')         
        bucket_name = environ.get('BUCKET_NAME')
        
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name) 

        blob.upload_from_filename(source_file_path)