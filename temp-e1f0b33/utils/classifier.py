import pandas as pd
from website.app.pages.api.user.models import Complaint
from utils.ml_pipeline import pipeline as ml_pipeline, complain_map
# from transformers import pipeline as hf_pipeline
from website.app.pages.api.user.database import SessionLocal

# Sentiment classifier
# sentiment_classifier = hf_pipeline("sentiment-analysis", framework="tf", model="distilbert-base-uncased-finetuned-sst-2-english")

def classify_user_complaints(user_id):
    """Classify only the current logged-in user's unclassified complaints."""
    print(f"Classifying complaints for user {user_id}")

    from website.app.pages.api.user.server import app as flask_app
    with flask_app.app_context():
        # unclassified = Complaint.query.filter_by(user_id=user_id, classification=None).all()
        
        # for complaint in unclassified:
        #     db = SessionLocal()
        #     try:
        #         complain_series = pd.Series([complaint.complaint])
        #         predicted_result = int(ml_pipeline.predict(complain_series)[0])
        #         category = complain_map[predicted_result]
        #         complaint.classification = category

        #         sentiment_result = sentiment_classifier(complaint.complaint)[0]
        #         complaint.sentiment = sentiment_result["label"]
        #         complaint.sentimentScore = sentiment_result["score"]

        #         db.session.commit()

        #     except Exception as e:
        #         print(f"Error classifying complaint ID {complaint.id}: {e}")
        #     finally:
        #         db.close()

        pass

