from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"

    id               = Column(Integer, primary_key=True, index=True)
    reviewer_name    = Column(String(100))
    product_name     = Column(String(100))
    product_category = Column(String(50))
    star_rating      = Column(Integer)
    review_text      = Column(Text)
    sentiment_label  = Column(String(20), nullable=True)
    sentiment_score  = Column(Float, nullable=True)
    topics           = Column(String(200), nullable=True)
    created_at       = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id            = Column(Integer, primary_key=True, index=True)
    review_id     = Column(Integer)
    z_score       = Column(Float)
    mean_score    = Column(Float)
    trigger_score = Column(Float)
    message       = Column(Text)
    created_at    = Column(DateTime, default=datetime.utcnow)