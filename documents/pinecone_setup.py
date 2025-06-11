from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )

index_name = "docfind-index"

#Check if index already exists, if not, create it
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
    )

#Connecting to index
index = pc.Index(index_name)

print("Pinecone index ready for use.")