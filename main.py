from src.answer import answer
from src.config import (
    EMBEDDING_MODEL,
    CHAT_MODEL,
    PINECONE_INDEX_NAME
)


def main():
    print("\n" + "=" * 55)
    print("       VECTRA LOGISTICS - IT SUPPORT ASSISTANT")
    print("=" * 55)

    print("\nConfiguration loaded successfully!")
    print("Embedding model:", EMBEDDING_MODEL)
    print("Chat model:", CHAT_MODEL)
    print("Pinecone index:", PINECONE_INDEX_NAME)

    print("\nAsk an IT support question.")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("\nThank you for using Vectra IT Support Assistant!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            result = answer(question)

            print("\nAssistant:", result["answer"])
            print("Citations:", result["citations"])
            print("Abstained:", result["abstained"])

        except Exception as error:
            print("\nAn error occurred:", str(error))


if __name__ == "__main__":
    main()
