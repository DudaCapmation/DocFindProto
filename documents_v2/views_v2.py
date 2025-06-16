from django.shortcuts import render
from documents.models import Document
from .vector_search_v2 import search_documents
from documents.azure_utils import generate_blob_url

def search_v2_view(request):
    query = request.GET.get("q", "")
    results = []


    # URL for downloading the whole document logic
    if query:
        matches = search_documents(query)

        for match in matches:
            try:
                doc = Document.objects.get(doc_id=match["doc_id"])
                blob_url = generate_blob_url(doc.blob_name)
                match["download_url"] = blob_url
            except Document.DoesNotExist:
                match["download_url"] = "#"

        results = matches

    return render(request, "search_v2.html", {"results": results})