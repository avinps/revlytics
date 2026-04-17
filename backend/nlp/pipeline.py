import logging
from backend.nlp.sentiment import analyze_sentiment
from backend.nlp.aspects import extract_aspects, aspects_to_string
from backend.nlp.anomaly import detector
from backend.db.models import Review
from backend.db.database import SessionLocal

logger = logging.getLogger(__name__)

def process_review(review_id: int) -> dict:
    db = SessionLocal()
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            logger.warning(f"Review {review_id} not found")
            return {}

        sentiment = analyze_sentiment(review.review_text)
        aspects   = extract_aspects(review.review_text)

        review.sentiment_label = sentiment["label"]
        review.sentiment_score = sentiment["score"]
        review.topics          = aspects_to_string(aspects)

        db.commit()

        alert = detector.add_review(
            review_id=review_id,
            label=sentiment["label"],
            score=sentiment["score"],
        )

        if alert:
            logger.warning(f"ALERT triggered by review {review_id}: {alert['message']}")

        logger.info(
            f"Review {review_id} processed — "
            f"{sentiment['label']} ({sentiment['score']}) | "
            f"topics: {review.topics or 'none'}"
        )

        return {
            "id":              review_id,
            "sentiment_label": review.sentiment_label,
            "sentiment_score": review.sentiment_score,
            "topics":          review.topics,
            "alert":           alert,
        }

    except Exception as e:
        logger.error(f"Error processing review {review_id}: {e}")
        db.rollback()
        return {}
    finally:
        db.close()