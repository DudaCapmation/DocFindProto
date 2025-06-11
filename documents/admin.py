from django.contrib import admin
from .models import Document

# Register your models here.

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'blob_name', 'doc_id')
    readonly_fields = ('blob_name', 'doc_id')