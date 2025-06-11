from django.shortcuts import render
from .vector_search import search_documents

# Create your views here.

def search_view(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = search_documents(query, top_k=5)

    return render(request, "search.html", {"results": results})
