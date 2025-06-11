from .embedding_utils import get_embeddings
from .pinecone_setup import index


def search_documents(query_text: str, top_k: int = 5):

    print(f"\nEmbedding query: {query_text!r}")
    query_vector = get_embeddings(query_text)
    print(f"Generated query embedding (first 5 dims): {query_vector[:5]}…")
    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    matches = response["matches"]

    results = []
    for match in matches:
        metadata = match.metadata
        snippet = metadata.get("text", "")[:300] + "…"  # Limiting to 300 characters
        results.append({
            "doc_id": metadata.get("doc_id"),
            "title": metadata.get("title"),
            "snippet": snippet,
            "score": match['score']
        })

    return results

if __name__ == "__main__":
    query = "Tell me about Agile Methodologies"
    results = search_documents(query, top_k=3)

    for result in results:
        print(f"\n{result['title']} (Score: {result['score']:.4f})")
        print(f"Snippet: {result['snippet']}\n")