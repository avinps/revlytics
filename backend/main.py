from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.db.database import create_tables
from backend.api import reviews, websocket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Revlytics API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    create_tables()
    logger.info("Preloading NLP models...")
    from backend.nlp.sentiment import load_sentiment_model
    load_sentiment_model()
    logger.info("Models ready")

app.include_router(reviews.router)
app.include_router(websocket.router)

@app.get("/health")
def health():
    return {"status": "ok"}