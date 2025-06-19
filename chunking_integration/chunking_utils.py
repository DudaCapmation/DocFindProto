import os
from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

def semantic_chunking(text: str, threshold_amount: int = 80):

    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

    text_splitter = SemanticChunker(embeddings,
                                    breakpoint_threshold_type="percentile",
                                    breakpoint_threshold_amount=threshold_amount)

    chunks = text_splitter.split_text(text)

    return chunks