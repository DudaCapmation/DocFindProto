import os

import cohere
from dotenv import load_dotenv
from documents.embedding_utils import get_embeddings
from documents.pinecone_setup import index

load_dotenv()

api_key = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(api_key)

def search_documents(query_text: str, top_k: int = 20, max_docs: int = 5):
    query_vector = get_embeddings(query_text)

    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    matches = response["matches"]

    doc_scores = {}
    doc_chunks = {}

    for match in matches:
        metadata = match.metadata or {}
        doc_id = metadata.get("doc_id")
        if not doc_id:
            continue

        score = match.score
        snippet = metadata.get("text", "")[:300] + "..."
        title = metadata.get("title", "Untitled")

        # Storing the best scoring chunk per doc_id
        if doc_id not in doc_scores or score > doc_scores[doc_id]:
            doc_scores[doc_id] = score
            doc_chunks[doc_id] = {
                "doc_id": doc_id,
                "title": title,
                "snippet": snippet,
                "score": score
            }

    # Sorting by best match score (descending)
    top_documents = sorted(doc_chunks.values(), key=lambda x: x["score"], reverse=True)

    #Cohere rerank
    rerank_inputs = [doc["snippet"] for doc in top_documents]

    rerank_response = co.rerank(
        model="rerank-v3.5",
        query=query_text,
        documents=rerank_inputs,
        top_n=len(top_documents)
    )

    rerank_sorted_results = []
    for result in rerank_response.results:
        rerank_sorted_results.append({
            **top_documents[result.index],
            "cohere_score": result.relevance_score
        })

    # Returning top N documents
    return rerank_sorted_results