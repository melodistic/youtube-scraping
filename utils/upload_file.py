import json
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
def upload_file_to_storage(env,filepath,mood):
    connection_str = env["connection_string"]
    print(connection_str)
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    container_name = "songwav"
    filename = os.path.basename(filepath)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.join(mood,filename))
    print("[upload] " + filename + " to Azure Blob Storage")
    with open(filepath, "rb") as data:
        blob_client.upload_blob(data)

if __name__ == "__main__":
    with open("env.json") as f:
        env = json.load(f)
    filename = "song/Romance/Hayden James - Just Friends (Official Video) ft. Boy Matthews.wav"
    upload_file_to_storage(env,filename,"Romance")