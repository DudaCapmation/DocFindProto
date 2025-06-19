from django.urls import path
from .views import semantic_chunking_api, extract_text_api

urlpatterns = [
    path('semantic-chunking/', semantic_chunking_api),
    path('extract-text/', extract_text_api),
]