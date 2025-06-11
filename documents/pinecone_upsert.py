import os
import uuid
import django

# Initializes Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from documents.models import Document
from embedding_utils import get_embeddings
from pinecone_setup import index
from azure_utils import download_blob_as_text
from chunking_utils import chunk_text

def upsert_documents():
    documents = Document.objects.all()

    for doc in documents:
        print(f"\nProcessing document: {doc.title}")

        try:

            # Downloading document from Azure using title as blob name
            full_text = download_blob_as_text(doc.title)

            chunks = chunk_text(full_text, chunk_size=500, overlap=100)

            vectors = []

            for i, chunk in enumerate(chunks):
                embedding = get_embeddings(chunk)
                chunk_id = str(uuid.uuid4())  # Unique ID per chunk

                vectors.append({
                    "id": chunk_id,
                    "values": embedding,
                    "metadata": {
                        "doc_id": str(doc.id),
                        "chunk_index": i,
                        "text": chunk,
                        "title": doc.title
                    }
                })

            # Upserting every chunk at once
            index.upsert(vectors)
            print(f"Uploaded {len(vectors)} chunks for '{doc.title}'")

            # Saving document's main doc_id
            doc.doc_id = str(doc.id)
            doc.save()

        except Exception as e:
            print(f"Error processing '{doc.title}': {e}")

    print("\nAll documents processed.")

if __name__ == "__main__":
    upsert_documents()