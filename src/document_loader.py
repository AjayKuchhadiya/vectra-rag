from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent
KB_DIR = BASE_DIR / "data" / "knowledge_base"

EXCLUDED_DOCS = {"KB-002", "KB-099"}


def load_documents():
    documents = []

    for file_path in KB_DIR.glob("*.md"):
        doc_id = file_path.name.split("_")[0]

        if doc_id in EXCLUDED_DOCS:
            print(f"Skipping: {doc_id}")
            continue

        raw_content = file_path.read_text(encoding="utf-8")

        # Extract YAML frontmatter separately
        metadata = {}

        match = re.match(
            r"\A---\s*\n(.*?)\n---\s*\n?",
            raw_content,
            re.DOTALL
        )

        if match:
            for line in match.group(1).splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()

            content = raw_content[match.end():].strip()
        else:
            content = raw_content.strip()

        documents.append({
            "doc_id": doc_id,
            "title": metadata.get("title", file_path.stem),
            "status": metadata.get("status", "unknown"),
            "effective_date": metadata.get("effective_date", ""),
            "owner": metadata.get("owner", ""),
            "content": content
        })

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print(f"\nLoaded {len(docs)} documents")

    for doc in docs:
        print(doc["doc_id"], "-", doc["title"])