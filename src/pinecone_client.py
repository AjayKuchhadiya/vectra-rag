from pinecone import Pinecone
from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME


def get_pinecone_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.index(PINECONE_INDEX_NAME)
    return index


if __name__ == "__main__":
    index = get_pinecone_index()

    print("Successfully connected to Pinecone!")
    print("Index:", PINECONE_INDEX_NAME)
    print("Index statistics:", index.describe_index_stats())