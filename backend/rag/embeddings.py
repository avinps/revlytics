import logging
import chromadb
from sentence_transformers import SentenceTransformer
from backend.db.database import SessionLocal
from backend.db.models import Review

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

_model  = None
_client = None
_collection = None

def get_embedding_model():
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("Embedding model loaded")
    return _model

def get_collection():
    global _client, _collection
    if _collection is None:
        _client     = chromadb.PersistentClient(path="./chromadb_store")
        _collection = _client.get_or_create_collection(
            name="reviews",
            metadata={"hnsw:space": "cosine"}
        )
    return _collection

def embed_review(review_id: int, text: str, metadata: dict):
    try:
        model      = get_embedding_model()
        collection = get_collection()

        existing = collection.get(ids=[str(review_id)])
        if existing["ids"]:
            return

        embedding = model.encode(text).tolist()
        collection.add(
            ids=[str(review_id)],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
        )
        logger.info(f"Embedded review {review_id}")
    except Exception as e:
        logger.error(f"Error embedding review {review_id}: {e}")

def embed_all_existing_reviews():
    db = SessionLocal()
    try:
        reviews = db.query(Review).filter(
            Review.sentiment_label != None
        ).all()

        collection = get_collection()
        existing   = collection.get()
        existing_ids = set(existing["ids"])

        count = 0
        for review in reviews:
            if str(review.id) in existing_ids:
                continue
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
            count += 1

        logger.info(f"Embedded {count} new reviews into ChromaDB")
        return count
    finally:
        db.close()

def get_collection_count() -> int:
    return get_collection().count()