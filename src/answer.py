
from src.retriever import retrieve_documents
from src.generator import generate_answer
from src.pii import redact_pii
from src.config import SIMILARITY_THRESHOLD

ABSTAIN_MESSAGE = (
    "I could not find this information in the knowledge base. "
    "Please raise an IT support ticket for assistance."
)


def abstain():
    return {
        "answer": ABSTAIN_MESSAGE,
        "citations": [],
        "abstained": True
    }


def answer(question):
    # 1. Retrieve relevant chunks

    # Redact PII before sending the question to external APIs
    safe_question = redact_pii(question)

    # Retrieve documents using the redacted question
    retrieved_chunks = retrieve_documents(safe_question)

    if not retrieved_chunks:
        return abstain()

    # 2. Apply the retrieval threshold
    highest_score = max(
        chunk["score"] for chunk in retrieved_chunks
    )

    if highest_score < SIMILARITY_THRESHOLD:
        return abstain()

    # 3. Generate structured answer
    result = generate_answer(safe_question, retrieved_chunks)

    # 4. Validate the response structure
    required_fields = {"answer", "citations", "abstained"}

    if not isinstance(result, dict):
        return abstain()

    if not required_fields.issubset(result):
        return abstain()

    if not isinstance(result["answer"], str):
        return abstain()

    if not isinstance(result["citations"], list):
        return abstain()

    if not isinstance(result["abstained"], bool):
        return abstain()

    # 5. If the model abstains, return a clean abstention
    if result["abstained"]:
        return abstain()

    # 6. Validate citations against retrieved document IDs
    retrieved_doc_ids = {
        chunk["doc_id"] for chunk in retrieved_chunks
    }

    model_citations = set(result["citations"])

    # Reject citations that were not retrieved
    if not model_citations.issubset(retrieved_doc_ids):
        return abstain()

    # An answer without supporting citations is not accepted
    if not model_citations:
        return abstain()

    # 7. Return the validated response
    return {
        "answer": result["answer"],
        "citations": sorted(model_citations),
        "abstained": False
    }


if __name__ == "__main__":
    questions = [
        "My VPN is showing error ZT-401. How can I fix it?",
        "How can I apply for a parking pass in Gurugram?"
    ]

    for question in questions:
        print("\nQuestion:", question)
        print("Final response:", answer(question))
