from documents.models import Document
from documents.azure_utils import generate_blob_url

def attach_download_urls(matches):

    # Attaches the Azure blob download URL to every match result.

    for match in matches:
        try:
            doc = Document.objects.get(doc_id=match["doc_id"])
            blob_url = generate_blob_url(doc.blob_name)
            match["download_url"] = blob_url
        except Document.DoesNotExist:
            match["download_url"] = "#"

    return matches