from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import Review
from backend.schemas.review import ReviewCreate, ReviewOut
from typing import List

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewOut)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/", response_model=List[ReviewOut])
def get_reviews(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    return db.query(Review).order_by(
        Review.created_at.desc()
    ).offset(skip).limit(limit).all()