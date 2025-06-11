def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

'''
# Testing
long_text = "This is a test sentence. " * 100
chunks = chunk_text(long_text, chunk_size=300, overlap=50)

for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i+1} ---\n{chunk}")
'''