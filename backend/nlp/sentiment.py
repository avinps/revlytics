from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

# ─── swap model here anytime ───────────────────────────────
SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
# other options:
# "cardiffnlp/twitter-roberta-base-sentiment-latest"  (more accurate, 500MB)
# "vader" (instant, no download, less accurate)
# ───────────────────────────────────────────────────────────

_sentiment_pipeline = None

def load_sentiment_model():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        logger.info(f"Loading sentiment model: {SENTIMENT_MODEL}")
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=SENTIMENT_MODEL,
            truncation=True,
            max_length=512,
        )
        logger.info("Sentiment model loaded successfully")
    return _sentiment_pipeline

def analyze_sentiment(text: str) -> dict:
    model = load_sentiment_model()
    result = model(text[:512])[0]

    label = result["label"].lower()
    score = round(result["score"], 4)

    if label == "positive":
        normalized = "positive"
    elif label == "negative":
        normalized = "negative"
    else:
        normalized = "neutral"

    return {
        "label": normalized,
        "score": score,
        "model": SENTIMENT_MODEL,
    }