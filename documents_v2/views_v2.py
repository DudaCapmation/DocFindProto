from django.shortcuts import render
from .vector_search_v2 import search_documents
from documents.utils import attach_download_urls

def search_v2_view(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        matches = search_documents(query)
        results = attach_download_urls(matches)

    return render(request, "search_v2.html", {"results": results})