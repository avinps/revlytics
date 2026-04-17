from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.db.database import get_db
from backend.db.models import Review, Alert

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/sentiment-summary")
def sentiment_summary(db: Session = Depends(get_db)):
    total     = db.query(Review).count()
    positive  = db.query(Review).filter(
        Review.sentiment_label == "positive"
    ).count()
    negative  = db.query(Review).filter(
        Review.sentiment_label == "negative"
    ).count()
    avg_score = db.query(func.avg(Review.sentiment_score)).scalar()
    avg_stars = db.query(func.avg(Review.star_rating)).scalar()

    return {
        "total_reviews": total,
        "positive":      positive,
        "negative":      negative,
        "neutral":       total - positive - negative,
        "avg_sentiment": round(float(avg_score or 0), 3),
        "avg_stars":     round(float(avg_stars or 0), 2),
        "positive_pct":  round(positive / total * 100, 1) if total else 0,
        "negative_pct":  round(negative / total * 100, 1) if total else 0,
    }

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(
        Alert.created_at.desc()
    ).limit(10).all()

    return {
        "total_alerts": db.query(Alert).count(),
        "alerts": [
            {
                "id":            a.id,
                "review_id":     a.review_id,
                "z_score":       a.z_score,
                "mean_score":    a.mean_score,
                "trigger_score": a.trigger_score,
                "message":       a.message,
                "created_at":    a.created_at.isoformat(),
            }
            for a in alerts
        ],
    }

@router.get("/topics")
def topic_breakdown(db: Session = Depends(get_db)):
    reviews = db.query(
        Review.topics,
        Review.sentiment_label
    ).filter(
        Review.topics != None,
        Review.topics != ""
    ).all()

    breakdown: dict = {}
    for topics_str, sentiment in reviews:
        if not topics_str:
            continue
        for topic in topics_str.split(","):
            topic = topic.strip()
            if topic not in breakdown:
                breakdown[topic] = {"positive": 0, "negative": 0, "total": 0}
            breakdown[topic]["total"] += 1
            if sentiment == "positive":
                breakdown[topic]["positive"] += 1
            elif sentiment == "negative":
                breakdown[topic]["negative"] += 1

    return {"topics": breakdown}