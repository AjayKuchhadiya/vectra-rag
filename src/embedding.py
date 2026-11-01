from openai import OpenAI

from src.config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_embeddings(texts):
    """
    Convert a list of text chunks into embeddings.
    """

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return [item.embedding for item in response.data]


if __name__ == "__main__":
    sample_text = [
        "How do I reset my password?",
        "What is the resolution SLA for a P2 ticket?"
    ]

    embeddings = generate_embeddings(sample_text)

    print("Number of embeddings:", len(embeddings))
    print("Vector dimensions:", len(embeddings[0]))
    print("First 5 values:", embeddings[0][:5])