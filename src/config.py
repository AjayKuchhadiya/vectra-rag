
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "vectra-it-support"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "text-embedding-3-small"
)

CHAT_MODEL = os.getenv(
    "CHAT_MODEL",
    "gpt-4.1-mini"
)

PINECONE_NAMESPACE = os.getenv(
    "PINECONE_NAMESPACE",
    "it-knowledge-base"
)

SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.25"))
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "1200"))
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "3"))
CHAT_TEMPERATURE = float(os.getenv("CHAT_TEMPERATURE", "0"))

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing")
