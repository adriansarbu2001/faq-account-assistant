# FAQ Account Assistant

An intelligent backend service that answers account-related questions using semantic search and AI-generated responses.  
The system retrieves the closest question-answer pair from a PostgreSQL knowledge base and, when no confident match is found, falls back to OpenAI via LangChain.

---

## Features

- **Semantic Search** powered by PostgreSQL + pgvector
- **OpenAI Fallback** through LangChain for unmatched queries
- **IT / Non-IT Router** for domain-aware routing
- **Celery + Redis** for asynchronous embedding computation
- **Structured Error Handling** for rate limits, upstream, and internal errors
- **Comprehensive Testing** with 100% coverage and clean code standards
- **Docker Compose + Makefile** for one-command setup and execution

---

## Architecture Overview

```
FastAPI (API)
│
├── /ask-question           <- Main endpoint
│         v
│   Router (IT / Non-IT)
│         v
│   Local Search (pgvector)
│         v
│         ├── Local Match -> Return local answer
│         └── No Match -> OpenAI Fallback (LangChain)
│
├── PostgreSQL + pgvector   <- Stores questions, answers, embeddings
├── Celery + Redis          <- Handles async embedding tasks
└── Docker Compose + Make   <- Orchestrates and simplifies setup
```

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/adriansarbu2001/faq-account-assistant.git
cd faq-account-assistant
```

### 2. Configure environment

Create an `.env` file based on `.env.example` and an `.env.docker` file based on `.env.docker.example`:
```bash
cp ./.env.example ./.env
cp ./infra/env/.env.docker.example ./infra/env/.env.docker
```

Edit the new environment files and set the openai api key with your key:
```env
OPENAI_API_KEY=<sk-your-key>
```

If we want to run the unit tests we need to create a local python environment aswell (python>=3.11) and install all dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## Quick Start (Makefile workflow)

```bash
make build              # Build all containers
make up                 # Start the full stack
make init-db            # Initialize the database schema
make seed-default       # Seed the default FAQ data from ./data/faq_seed.json
make update-embeddings  # Compute and fill in the embeddings for each question
```

Check health:
```bash
make health
# {"status":"ok"}
```

---

## API Usage

### Ask a question
```bash
curl -X POST http://localhost:8000/ask-question -H "Authorization: Bearer dev-token" -H "Content-Type: application/json" -d '{"user_question": "Can I change my email?"}'
```

### Example responses

**Local match found**
```json
{
    "source": "local",
    "matched_question": "Is it possible to change my registered email address?",
    "answer": "Yes, navigate to account settings, find the 'Change Email' option, enter your new email, and follow the verification process."
}
```

**Fallback to OpenAI**
```json
{
    "source": "openai",
    "matched_question": "N/A",
    "answer": "Yes, you can change your email in your account settings. Look for the \"Account\" or \"Profile\" section, then find the option to update your email address. If you're unsure, check the help section for specific instructions related to your account type."
}
```

**Non-IT / Compliance route**
```json
{
    "source": "local",
    "matched_question": "N/A",
    "answer": "This is not really what I was trained for, therefore I cannot answer. Try again."
}
```

---

## Testing

Use PyTest to run the unit tests:

```bash
pytest --cov
```

---

## Tech Stack

**Core:** FastAPI, PostgreSQL, pgvector, LangChain  
**Async:** Celery, Redis  
**Infrastructure:** Docker Compose, Make  
**ORM & Config:** SQLAlchemy, Pydantic Settings  
**Testing & Quality:** pytest, Ruff, MyPy, Black  

---

## Author

**Adrian-Mihai Sârbu**  
M.Sc., AI Engineer  
[LinkedIn](https://www.linkedin.com/in/adrian-sarbu-0a132b166) • [GitHub](https://github.com/adriansarbu2001)
