from src.retriever import retrieve_documents

question = "My laptop is slow. Should I disable antivirus or Windows Defender permanently?"

results = retrieve_documents(question)

for result in results:
    print("Document:", result["doc_id"])
    print("Score:", round(result["score"], 4))
    print("Content:")
    print(result["text"])
    print("-" * 50)