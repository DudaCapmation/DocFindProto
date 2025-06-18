from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

def get_blob_client(connection_str, container_name, blob_name):

    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    container_client = blob_service_client.get_container_client(container_name)

    return container_client.get_blob_client(blob_name)

def get_blob_client_headers(request):
    connection_string = request.headers.get("X-Connection-String")
    container_name = request.headers.get("X-Container-Name")
    blob_name = request.headers.get("X-Blob-Name")

    if not all([connection_string, container_name, blob_name]):
        raise ValueError("Missing required headers: X-Connection-String, X-Container-Name, X-Blob-Name")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    return container_client.get_blob_client(blob_name)

@api_view(['PUT'])
def azure_create_or_update(request):

    try:
        blob_client = get_blob_client_headers(request)
        file = request.body
        blob_client.upload_blob(file.read(), overwrite=True)

        return Response({"message": "Upload successful"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def azure_delete(request):

    try:
        connection_string = request.data["connection_string"]
        container_name = request.data["container_name"]
        blob_name = request.data["blob_name"]

        blob_client = get_blob_client(connection_string, container_name, blob_name)
        blob_client.delete_blob()

        return Response({"message": "Deletion successful"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def azure_get(request):
    try:
        connection_string = request.data["connection_string"]
        container_name = request.data["container_name"]
        blob_name = request.data["blob_name"]

        blob_client = get_blob_client(connection_string, container_name, blob_name)
        content = blob_client.download_blob().readall().decode('utf-8')

        return Response({"content": content}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def azure_get_url(request):
        try:
            connection_string = request.data["connection_string"]
            container_name = request.data["container_name"]
            blob_name = request.data["blob_name"]

            blob_client = BlobServiceClient.from_connection_string(connection_string)
            sas_token = generate_blob_sas(
                account_name=blob_client.account_name,
                container_name=container_name,
                blob_name=blob_name,
                account_key=blob_client.credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1)
            )

            blob_url = f"{blob_client.url}?{sas_token}"

            return Response({"url": blob_url}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
