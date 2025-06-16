from django.urls import path
from .views import search_view
from documents_v2.views_v2 import search_v2_view

urlpatterns = [
    path("search/", search_view, name="search"),
    path("search/v2/", search_v2_view, name="search_v2"),
]