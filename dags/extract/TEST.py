import os
import google.cloud.storage as storage

def blob_data(point_dir):

    json_path = '/Users/kimdohoon/Downloads/abstract-robot-390510-cb4515df5695.json'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path

    client = storage.Client()
    bucket_name = 'scouter-dl'
    bucket = client.get_bucket(bucket_name)

    local_directory = point_dir

    for dirpath, dirs, files in os.walk(local_directory):
        for file_name in files:
            local_file_path = os.path.join(dirpath, file_name)
        
            gcs_object_name = local_file_path.replace(local_directory, '')
            gcs_object_name = gcs_object_name.replace(os.path.sep, '2022/fixtures-events/')
            
            blob = bucket.blob(gcs_object_name)
            with open(local_file_path, 'rb') as file:
                load_blob = blob.upload_from_file(file)
                print(f"{local_file_path} uploaded to gs://{bucket_name}/{gcs_object_name}")

if __name__ == "__main__":
    blob_data('/Users/kimdohoon/desktop')