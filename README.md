# JUWORKSHOP_JAN_2026

> RAG portion inspired by Pamela Fox's [`learnlive-rag-starter`](https://github.com/pamelafox/learnlive-rag-starter) workshop repo.

<p align="center">RAG experiments and Qdrant ingestion workbench from the January 2026 workshop.</p>

> - `agent-framework-core` material is sourced directly from the [`ambarishg/agent-framework`](https://github.com/ambarishg/agent-framework).

## Overview
- `RAG/` contains lightweight retrieval pipelines that demonstrate how to query the pre-ingested insect corpus (`rag_ingested_chunks.json`) with Lunr and Azure OpenAI.
- `QDRANT/` holds tooling to split a PDF, generate embeddings with Azure OpenAI, and push them into a Qdrant collection.
- Python dependencies are managed via `requirements.txt`; the project expects Azure OpenAI credentials and (for Qdrant flows) a hosted Qdrant instance.


## Prerequisites
1. Install Python 3.12+ and a terminal that can run PowerShell or Bash on Windows.
2. Provision an Azure OpenAI deployment and note the `endpoint` and `deployment id`. Growth of both folders assumes you can authenticate via `DefaultAzureCredential`.
3. (Optional) Stand up a Qdrant cloud/standalone service and capture its HTTP `HOST` and `API_KEY` if you want to ingest data into a vector store.

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Environment variables
- `RAG/.env` should contain `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_DEPLOYMENT_ID` so `RAG/config.py` can wire up `AIProjectClient`.
- `QDRANT/.env` needs `HOST`, `API_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_DEPLOYMENT_ID` for the notebook and `config_qdrant.py`.

Use `python-dotenv` to load the variables; no sample `.env` is included to keep secrets out of source control.

## Key workflows
- `python RAG/rag_documents_flow.py`: loads `rag_ingested_chunks.json` from `RAG/`, searches the Lunr index for the hard-coded question, and routes the top contexts into Azure OpenAI via `client.chat.completions.create`. You can adapt `user_question` or rewrite the system prompt.
- `RAG/rag_documents_hybrid.py` / `rag_documents_ingestion.py` / `rag_multiturn.py` / `rag_queryrewrite.py`: additional demonstrations of ingestion patterns, multiturn context, and query rewriting that share the same `get_model.py`/config wiring.
- `QDRANT/ingest.ipynb`: converts `RAG/data/Western_honey_bee.pdf` to markdown with `pymupdf4llm`, splits it into chunks with `RecursiveCharacterTextSplitter`, generates embeddings using `text-embedding-3-small`, and uploads them in batches to the named Qdrant collection. Open the notebook in VS Code or Jupyter to step through the cells.

## Data & artifacts
- `RAG/data/` currently holds `Western_honey_bee.pdf` and any other raw source PDFs you want to index. This repo also ships `RAG/rag_ingested_chunks.json`, which is consumed by the Lunr examples and is excluded via `.gitignore` once regenerated.
- Keep large JSON dumps, `.env` files, and model outputs local; they are ignored by `.gitignore`.

## Tips
1. When you update the Azure deployment or switch to a new region, refresh both `.env` files and restart the virtual environment before running the notebooks.
2. Re-ingest to a Qdrant collection only after cleaning old points or renaming the collection (the notebook assumes `COLLECTION_NAME = "BEES"`).
3. Use `pip install --upgrade pip` inside `.venv` before installing requirements to avoid legacy wheel errors.

Feel free to extend the notebooks/scripts with LangChain agents or new PDFs as the workshop continues.
