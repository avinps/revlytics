from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReviewCreate(BaseModel):
    reviewer_name:    str
    product_name:     str
    product_category: str
    star_rating:      int
    review_text:      str

class ReviewOut(BaseModel):
    id:               int
    reviewer_name:    str
    product_name:     str
    product_category: str
    star_rating:      int
    review_text:      str
    sentiment_label:  Optional[str]
    sentiment_score:  Optional[float]
    topics:           Optional[str]
    created_at:       datetime

    class Config:
        from_attributes = True