from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embeddings(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

'''
# Test
query = "Find documents about AI"
vector = get_embeddings(query)

print("Embedding vector size:", len(vector))
print("First 5 numbers:", vector[:5])
'''