import logging
from collections import deque
from statistics import mean, stdev
from datetime import datetime

logger = logging.getLogger(__name__)

WINDOW_SIZE    = 50
ALERT_THRESHOLD = 2.0

class AnomalyDetector:
    def __init__(self):
        self.window: deque = deque(maxlen=WINDOW_SIZE)
        self.alert_active  = False

    def _sentiment_to_score(self, label: str, score: float) -> float:
        if label == "positive":
            return score
        elif label == "negative":
            return -score
        else:
            return 0.0

    def add_review(self, review_id: int, label: str, score: float) -> dict | None:
        numeric_score = self._sentiment_to_score(label, score)
        self.window.append(numeric_score)

        if len(self.window) < 20:
            return None

        current_mean = mean(self.window)
        current_std  = stdev(self.window) if len(self.window) > 1 else 0

        if current_std == 0:
            return None

        z_score = (numeric_score - current_mean) / current_std

        if z_score < -ALERT_THRESHOLD and not self.alert_active:
            self.alert_active = True
            alert = {
                "type":          "sentiment_drop",
                "review_id":     review_id,
                "z_score":       round(z_score, 3),
                "mean":          round(current_mean, 3),
                "score":         round(numeric_score, 3),
                "timestamp":     datetime.utcnow().isoformat(),
                "message":       f"Sentiment spike detected — score {round(numeric_score, 3)} is {round(abs(z_score), 1)} std devs below average"
            }
            self._save_alert(review_id, z_score, current_mean, numeric_score, alert["message"])
            logger.warning(f"ANOMALY ALERT: {alert['message']}")
            return alert

        if z_score > -1.0:
            self.alert_active = False

        return None

    def _save_alert(self, review_id, z_score, mean_score, trigger_score, message):
        try:
            from backend.db.database import SessionLocal
            from backend.db.models import Alert
            db = SessionLocal()
            alert = Alert(
                review_id=review_id,
                z_score=round(z_score, 3),
                mean_score=round(mean_score, 3),
                trigger_score=round(trigger_score, 3),
                message=message,
            )
            db.add(alert)
            db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Failed to save alert: {e}")

    def get_stats(self) -> dict:
        if not self.window:
            return {"mean": 0, "std": 0, "window_size": 0}
        return {
            "mean":         round(mean(self.window), 3),
            "std":          round(stdev(self.window), 3) if len(self.window) > 1 else 0,
            "window_size":  len(self.window),
            "alert_active": self.alert_active,
        }

detector = AnomalyDetector()