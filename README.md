# Revlytics 🔍

> A real-time customer review analytics platform that transforms raw reviews into actionable intelligence powered by NLP, RAG-based conversational AI, and live WebSocket streaming.

![Status](https://img.shields.io/badge/status-active%20development-brightgreen)
![Python](https://img.shields.io/badge/python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-teal)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## What is Revlytics?

Most businesses drown in customer reviews. Revlytics turns that flood into a real-time intelligence feed surfacing sentiment trends, detecting crises before they escalate, and letting anyone on the team ask plain-English questions about what customers are actually saying.

Built end-to-end as a production-grade system: event-driven data ingestion, an NLP analysis engine, a RAG-powered conversational layer, and a live React dashboard.

---

## Live Demo
> 🔗 Coming soon — deploying after Phase 4

---

## Architecture

```
Review Stream (WebSocket)
        ↓
FastAPI Ingest Layer
        ↓
NLP Pipeline (HuggingFace)
  ├── Sentiment Analysis
  ├── Aspect Extraction
  ├── Topic Clustering
  └── Anomaly Detection
        ↓
PostgreSQL + ChromaDB (Vector Store)
        ↓
RAG Layer (LangChain + HuggingFace)
        ↓
React Dashboard (Live Charts + AI Query Bar)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, Python 3.13, async/await |
| Real-time streaming | WebSocket, Server-Sent Events |
| Database | PostgreSQL, SQLAlchemy |
| NLP / ML | HuggingFace Transformers, sentence-transformers |
| Vector store | ChromaDB |
| RAG pipeline | LangChain, BM25 + semantic hybrid search |
| Frontend | React, Recharts, D3 |
| MLOps | Docker, GitHub Actions CI/CD |
| Experiment tracking | Weights & Biases |
| Deployment | Railway (backend), Vercel (frontend) |

---

## Development Roadmap

### ✅ Phase 1 — Real-time Data Pipeline (Complete)
- [x] FastAPI backend with modular architecture
- [x] Realistic fake review generator (Faker.js-style, Python)
- [x] WebSocket endpoint streaming reviews in real time
- [x] PostgreSQL database with SQLAlchemy ORM
- [x] REST API with full interactive docs (`/docs`)
- [x] Reviews persisted automatically as they stream in

---

### 🚧 Phase 2 — NLP Analysis Engine (In Progress)
- [ ] Sentiment analysis per review using HuggingFace Transformers
- [ ] Aspect-based sentiment extraction (shipping, quality, support, price)
- [ ] Topic clustering with sentence-transformers + k-means
- [ ] Anomaly detection — Z-score alert when sentiment drops suddenly
- [ ] Star rating vs text sentiment mismatch detector
- [ ] Batched inference pipeline (processes reviews every 500ms)
- [ ] Experiment tracking with Weights & Biases

---

### 📋 Phase 3 — RAG Conversational Layer (Upcoming)
- [ ] ChromaDB vector store — every review embedded on arrival
- [ ] Hybrid search: BM25 keyword + semantic vector retrieval
- [ ] Re-ranking with metadata filters (date, stars, product, topic)
- [ ] LangChain Q&A chain with cited answers
- [ ] Natural language queries: *"Why are customers upset about shipping?"*
- [ ] Auto-generated weekly AI digest with actionable suggestions
- [ ] LangSmith observability for RAG chain tracing

---

### 📋 Phase 4 — React Dashboard (Upcoming)
- [ ] Live review feed with sentiment badges and topic tags
- [ ] Sentiment timeline chart (zoomable, filterable)
- [ ] Topic heatmap — frequency × sentiment grid
- [ ] Anomaly alert banner with trigger reviews
- [ ] Star rating distribution histogram
- [ ] Natural language query bar (hits RAG endpoint)
- [ ] Side-by-side comparison mode (two products / two time periods)
- [ ] Smart filters (date, rating, sentiment, topic, category)
- [ ] Mismatch detector view (sarcasm / fake review surface)
- [ ] Priority response queue for urgent reviews

---

### 📋 Phase 5 — MLOps + Deployment (Upcoming)
- [ ] Dockerize all services (FastAPI, ChromaDB, PostgreSQL, React)
- [ ] Docker Compose for single-command local setup
- [ ] GitHub Actions CI/CD pipeline
- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Vercel
- [ ] AWS Lambda for NLP inference endpoint
- [ ] S3 for review archive storage
- [ ] Full README with architecture diagram and demo video

---

## Project Structure

```
revlytics/
├── backend/
│   ├── main.py               # FastAPI app entry point
│   ├── api/
│   │   ├── reviews.py        # REST endpoints
│   │   ├── websocket.py      # WebSocket live stream
│   │   ├── analytics.py      # Sentiment + topic endpoints
│   │   └── rag.py            # RAG query endpoint
│   ├── core/
│   │   ├── config.py         # Environment config
│   │   └── generator.py      # Fake review generator
│   ├── db/
│   │   ├── database.py       # DB connection + session
│   │   └── models.py         # SQLAlchemy models
│   ├── nlp/                  # NLP pipeline (Phase 2)
│   └── rag/                  # RAG pipeline (Phase 3)
├── frontend/                 # React dashboard (Phase 4)
├── .env.example
├── requirements.txt
└── README.md
```

---

## Key Features (When Complete)

- **Real-time ingestion** — reviews stream in via WebSocket at configurable rate
- **Aspect-based NLP** — per-topic sentiment, not just overall positive/negative
- **Anomaly detection** — automatic alerts when sentiment drops suddenly
- **Conversational AI** — ask plain-English questions, get cited answers from real reviews
- **Mismatch detection** — surfaces sarcastic and potentially fake reviews
- **Priority queue** — auto-ranks reviews that need urgent responses
- **Export reports** — PDF/CSV exports for team sharing

---

## Why This Project?

Built to demonstrate my end-to-end ML engineering skills relevant to production environments:
- Event-driven architecture with real-time data pipelines
- NLP inference pipeline with batching and performance optimization
- RAG system with hybrid retrieval and observability
- Full MLOps lifecycle: experiment tracking → containerization → CI/CD → cloud deployment

