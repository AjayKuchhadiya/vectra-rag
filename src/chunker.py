import re


def split_into_sections(content):
    """
    Split Markdown content using headings.
    Each section retains its heading.
    """

    sections = re.split(
        r"(?m)(?=^#{1,3}\s)",
        content
    )

    return [
        section.strip()
        for section in sections
        if section.strip()
    ]


def chunk_document(document, max_chunk_size=1200):

    sections = split_into_sections(document["content"])

    # Merge standalone headings with the following section
    merged_sections = []
    pending_heading = ""

    for section in sections:
        section = section.strip()

        if re.fullmatch(r"#{1,3}\s+.+", section):
            pending_heading += section + "\n\n"
            continue

        if pending_heading:
            section = pending_heading + section
            pending_heading = ""

        merged_sections.append(section)

    # Handle a heading at the very end of a document
    if pending_heading:
        if merged_sections:
            merged_sections[-1] += "\n\n" + pending_heading
        else:
            merged_sections.append(pending_heading)

    chunks = []
    chunk_number = 0

    for section in merged_sections:

        if len(section) <= max_chunk_size:
            chunks.append({
                "doc_id": document["doc_id"],
                "title": document["title"],
                "status": document["status"],
                "effective_date": document["effective_date"],
                "owner": document["owner"],
                "chunk_id": f"{document['doc_id']}-{chunk_number}",
                "text": section
            })

            chunk_number += 1

        else:
            paragraphs = section.split("\n\n")
            current_chunk = ""

            for paragraph in paragraphs:
                candidate = (
                    current_chunk + "\n\n" + paragraph
                ).strip()

                if len(candidate) > max_chunk_size and current_chunk:
                    chunks.append({
                        "doc_id": document["doc_id"],
                        "title": document["title"],
                        "status": document["status"],
                        "effective_date": document["effective_date"],
                        "owner": document["owner"],
                        "chunk_id": f"{document['doc_id']}-{chunk_number}",
                        "text": current_chunk
                    })

                    chunk_number += 1
                    current_chunk = paragraph
                else:
                    current_chunk = candidate

            if current_chunk.strip():
                chunks.append({
                    "doc_id": document["doc_id"],
                    "title": document["title"],
                    "status": document["status"],
                    "effective_date": document["effective_date"],
                    "owner": document["owner"],
                    "chunk_id": f"{document['doc_id']}-{chunk_number}",
                    "text": current_chunk
                })

                chunk_number += 1

    return chunks

def chunk_documents(documents):
    """
    Chunk all loaded documents.
    """

    all_chunks = []

    for document in documents:
        document_chunks = chunk_document(document)
        all_chunks.extend(document_chunks)

    return all_chunks


if __name__ == "__main__":
    from src.document_loader import load_documents

    documents = load_documents()
    chunks = chunk_documents(documents)

    print(f"\nTotal documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks:
        print("\n----------------------------")
        print("Chunk ID:", chunk["chunk_id"])
        print("Document:", chunk["doc_id"])
        print("Characters:", len(chunk["text"]))
        print("Content preview:")
        print(chunk["text"][:200])