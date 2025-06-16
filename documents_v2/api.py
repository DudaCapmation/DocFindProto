from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .vector_search_v2 import search_documents

@api_view(['GET'])

def search_v2_api(request):
    query = request.GET.get('q')
    if not query:
        return Response({"error": "Missing query parameter"}, status=status.HTTP_400_BAD_REQUEST)

    results = search_documents(query)
    return Response(results, status=status.HTTP_200_OK)