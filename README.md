# Vectra Logistics IT Support Assistant

A retrieval-augmented assistant that answers employee IT questions using a
Markdown knowledge base. It retrieves relevant content from Pinecone, generates
grounded answers with OpenAI, redacts common PII from questions before external
calls, and abstains when it cannot provide a supported answer.

## Requirements

- Python
- OpenAI API key
- Pinecone API key and a Pinecone index configured for the embedding model

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   On macOS or Linux, activate it with `source .venv/bin/activate`.

2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set your API keys and configuration:

   ```text
   OPENAI_API_KEY=...
   PINECONE_API_KEY=...
   ```

   The example file includes the default models, index name, namespace, and
   retrieval settings. Update them to match your Pinecone index as needed.

4. Add approved Markdown knowledge-base documents to
   `data/knowledge_base/`. The loader reads Markdown files from this folder;
   documents with IDs `KB-002` and `KB-099` are excluded from ingestion.

   **Note:** `data/` is excluded by `.gitignore`. Knowledge-base files must be
   supplied locally and will not be included in Git by default.

## Ingest the knowledge base

After configuring `.env`, populate the Pinecone namespace with the knowledge
base:

```powershell
python -m src.ingest
```

Ingestion loads the Markdown documents, splits them into chunks, generates
embeddings, and upserts the chunks into Pinecone.

## Run the assistant

Start the interactive command-line assistant:

```powershell
python main.py
```

Enter an IT support question, or type `exit` or `quit` to stop. Answers include
citations to supporting knowledge-base documents. The assistant abstains if
retrieval or generated content does not meet its validation requirements.

## Evaluation and checks

Run the evaluation set:

```powershell
python evaluate.py
```

This sends questions to the configured OpenAI and Pinecone services and reports
citation, abstention, and keyword checks.

The PII redaction integration check uses mocks and does not make external API
calls:

```powershell
python -m tests.test_pii_integration
```

These scripts use the configured services and make external API calls:

```powershell
python -m tests.test_retrieval
python -m tests.test_prompt_injection
```

## Configuration

The main settings are read from `.env`:

| Variable | Default | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | — | Required OpenAI API key |
| `PINECONE_API_KEY` | — | Required Pinecone API key |
| `PINECONE_INDEX_NAME` | `vectra-it-support` | Pinecone index name |
| `PINECONE_NAMESPACE` | `it-knowledge-base` | Namespace used for ingestion and retrieval |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | OpenAI embedding model |
| `CHAT_MODEL` | `gpt-4.1-mini` | OpenAI chat model |
| `SIMILARITY_THRESHOLD` | `0.25` | Minimum retrieval score to generate an answer |
| `RETRIEVAL_TOP_K` | `3` | Maximum number of chunks retrieved |
| `MAX_CHUNK_SIZE` | `1200` | Maximum chunk size in characters |
| `CHAT_TEMPERATURE` | `0` | Chat model temperature |
