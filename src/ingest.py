from src.document_loader import load_documents
from src.chunker import chunk_documents
from src.embedding import generate_embeddings
from src.pinecone_client import get_pinecone_index

NAMESPACE = "it-knowledge-base"


def ingest_documents():
    # Step 1: Load approved documents
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")

    # Step 2: Convert documents into chunks
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks")

    # Step 3: Generate embeddings
    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)
    print(f"Generated {len(embeddings)} embeddings")

        # Step 4: Prepare documents for Pinecone Documents API
    documents_to_upsert = []

    for chunk, embedding in zip(chunks, embeddings):
        documents_to_upsert.append({
            "_id": chunk["chunk_id"],
            "embeddings": embedding,
            "doc_id": chunk["doc_id"],
            "title": chunk["title"],
            "status": chunk["status"],
            "effective_date": chunk["effective_date"],
            "owner": chunk["owner"],
            "text": chunk["text"]
        })

    # Step 5: Upsert documents into Pinecone
    index = get_pinecone_index()

    response = index.documents.upsert(
        namespace=NAMESPACE,
        documents=documents_to_upsert
    )

    print("\nIngestion completed!")
    print("Upserted documents:", response.upserted_count)

    # Step 6: Verify Pinecone
    stats = index.describe_index_stats()
    print("\nPinecone index statistics:")
    print(stats)


if __name__ == "__main__":
    ingest_documents()