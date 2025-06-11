from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.core.exceptions import ResourceExistsError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "docfind-container"

'''
CONTAINER TEST:

client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
containers = client.list_containers()

print("Available containers:")
for container in containers:
    print(container["name"])
'''


def download_blob_as_text(blob_name):

    # Initializing the client
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    stream = blob_client.download_blob()

    # Reading and decoding the content
    return stream.readall().decode('utf-8')

# Creates container if it doesn't exist
def create_container(blob_service_client: BlobServiceClient, container_name: str):
    try:
        container_client = blob_service_client.create_container(name=container_name)
        print(f"Created Azure container: {container_name}")
    except ResourceExistsError:
        print(f"A container named '{container_name}' already exists.")

def upload_blob(file, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
    create_container(blob_service_client, container_name)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(file, overwrite=True)

    # Returning blob url for OCR
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"

    print(f"Uploaded blob: {blob_name}")
    return blob_url

def generate_blob_url(blob_name: str, expires_in_minutes=30) -> str:
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    sas_token = generate_blob_sas(
        account_name=blob_client.account_name,
        container_name=blob_client.container_name,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    )

    return f"{blob_client.url}?{sas_token}"