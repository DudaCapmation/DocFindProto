from django.urls import path
from .views import azure_create_or_update, azure_delete, azure_get, azure_get_url

urlpatterns = [
    path('create/', azure_create_or_update),
    path('delete/', azure_delete),
    path('get/', azure_get),
    path('get-url/', azure_get_url),
]