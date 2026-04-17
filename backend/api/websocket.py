import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.core.generator import generate_review
from backend.db.database import SessionLocal
from backend.db.models import Review
from backend.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(tags=["websocket"])
executor = ThreadPoolExecutor(max_workers=2)

class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, data: dict):
        for ws in self.active.copy():
            try:
                await ws.send_json(data)
            except Exception:
                self.active.remove(ws)

manager = ConnectionManager()

def run_nlp_and_embed(review_id: int):
    try:
        from backend.nlp.pipeline import process_review
        result = process_review(review_id)
        if result.get("sentiment_label"):
            from backend.rag.embeddings import embed_review
            from backend.db.database import SessionLocal
            from backend.db.models import Review
            db = SessionLocal()
            try:
                review = db.query(Review).filter(Review.id == review_id).first()
                if review:
                    embed_review(
                        review_id=review.id,
                        text=review.review_text,
                        metadata={
                            "star_rating":      review.star_rating,
                            "sentiment_label":  review.sentiment_label or "",
                            "sentiment_score":  float(review.sentiment_score or 0),
                            "product_name":     review.product_name,
                            "product_category": review.product_category,
                            "topics":           review.topics or "",
                            "created_at":       review.created_at.isoformat(),
                        }
                    )
            finally:
                db.close()
    except Exception as e:
        logger.error(f"NLP+embed error for review {review_id}: {e}")

@router.websocket("/ws/reviews")
async def review_stream(websocket: WebSocket):
    await manager.connect(websocket)
    loop = asyncio.get_event_loop()
    try:
        while True:
            review = generate_review()
            db = SessionLocal()
            try:
                db_review = Review(**review.model_dump())
                db.add(db_review)
                db.commit()
                db.refresh(db_review)
                review_id = db_review.id

                payload = {
                    "id":               db_review.id,
                    "reviewer_name":    db_review.reviewer_name,
                    "product_name":     db_review.product_name,
                    "product_category": db_review.product_category,
                    "star_rating":      db_review.star_rating,
                    "review_text":      db_review.review_text,
                    "created_at":       db_review.created_at.isoformat(),
                }
                await manager.broadcast(payload)
            finally:
                db.close()

            loop.run_in_executor(executor, run_nlp_and_embed, review_id)
            await asyncio.sleep(1 / settings.review_stream_rate)

    except WebSocketDisconnect:
        manager.disconnect(websocket)