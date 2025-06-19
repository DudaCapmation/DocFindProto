from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .chunking_utils import semantic_chunking
from .ocr_utils import extract_text_from_document_url

@api_view(['POST'])
def semantic_chunking_api(request):

    try:
        text = request.data["text"]
        threshold_amount = request.data["threshold_amount"]

        if not text:
            return Response({"error": "Missing 'text' field"}, status=status.HTTP_400_BAD_REQUEST)

        chunks = semantic_chunking(text, threshold_amount)

        return  Response({"chunks": chunks}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def extract_text_api(request):

    try:
        url = request.data["url"]

        if not url:
            return Response({"error": "Missing 'url' field"}, status=status.HTTP_400_BAD_REQUEST)

        text = extract_text_from_document_url(url)

        return  Response({"text": text}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
