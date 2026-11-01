
from pinecone import DenseVectorQuery

from src.config import PINECONE_NAMESPACE, RETRIEVAL_TOP_K
from src.embedding import generate_embeddings
from src.pinecone_client import get_pinecone_index

VECTOR_FIELD = "embeddings"


def retrieve_documents(question, top_k=RETRIEVAL_TOP_K):
    """
    Retrieve relevant knowledge-base chunks using
    OpenAI embeddings and Pinecone document search.
    """

    # 1. Convert the question into an embedding
    query_embedding = generate_embeddings([question])[0]

    # 2. Connect to Pinecone
    index = get_pinecone_index()

    # 3. Search the document index
    results = index.documents.search(
        namespace=PINECONE_NAMESPACE,
        top_k=top_k,
        score_by=[
            DenseVectorQuery(
                field=VECTOR_FIELD,
                values=query_embedding
            )
        ],
        include_fields=["doc_id", "title", "text"]
    )

    # 4. Extract matching documents
    retrieved_chunks = []

    for hit in results.matches:
        retrieved_chunks.append({
            "doc_id": hit.get("doc_id", ""),
            "score": hit.score,
            "text": hit.get("text", ""),
            "title": hit.get("title", "")
        })

    return retrieved_chunks


if __name__ == "__main__":

    question = "My VPN is showing error ZT-401. How can I fix it?"

    results = retrieve_documents(question)

    print("\nUser question:", question)
    print("\nRetrieved documents:")

    for result in results:
        print("\n-----------------------------")
        print("Document ID:", result["doc_id"])
        print("Similarity score:", result["score"])
        print("Title:", result["title"])
        print("Content:")
        print(result["text"])
