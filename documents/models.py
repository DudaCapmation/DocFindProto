from django.db import models
from .azure_utils import upload_blob, generate_blob_url
from .chunking_utils import chunk_text
from .embedding_utils import get_embeddings
from .pinecone_setup import index
from chunking_integration.ocr_utils import extract_text_from_document_url
import uuid

# Create your models here.

class Document(models.Model):
    doc_id = models.CharField(max_length=500, blank=True, null=True, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True) # Optional if from Azure

    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    blob_name = models.CharField(max_length=300, blank=True, null=True)  # Storing Azure blob name

    def save(self, *args, **kwargs):
        if self.file:
            blob_name = self.file.name
            upload_blob(self.file, blob_name)
            self.blob_name = blob_name
        super().save(*args, **kwargs)

        # Autofill doc_id if it's empty
        if not self.doc_id:
            self.doc_id = str(self.id)
            super().save(update_fields=["doc_id"])

        blob_url = generate_blob_url(self.blob_name)

        # Extract text with Mistral OCR
        full_text = extract_text_from_document_url(blob_url)
        self.content = full_text

        # Chunking
        chunks = chunk_text(full_text, chunk_size=500, overlap=100)

        # Upserting each chunk to Pinecone
        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = get_embeddings(chunk)
            chunk_id = str(uuid.uuid4())
            vectors.append({
                "id": chunk_id,
                "values": embedding,
                "metadata": {
                    "doc_id": self.doc_id,
                    "chunk_index": i,
                    "text": chunk,
                    "title": self.title
                }
            })

        index.upsert(vectors)
        print(f"Upserted {len(vectors)} chunks for '{self.title}'")

        super().save(update_fields=['content'])  # Updating saved content

    def __str__(self):
        return self.title