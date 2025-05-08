import pandas as pd
# from website.app.pages.api.user.models import db, Complaint
from utils.ml_pipeline import pipeline as ml_pipeline, complain_map
from transformers import pipeline as hf_pipeline

from database.lib.prisma import prisma

# Sentiment classifier
sentiment_classifier = hf_pipeline("sentiment-analysis", framework="tf", model="distilbert-base-uncased-finetuned-sst-2-english")

async def classify_user_complaints(user_id):
    """Classify only the current logged-in user's unclassified complaints."""
    print(f"Classifying complaints for user {user_id}")

    try:
        unclassified = await prisma.complaint.find_many(
            where={
                "user_id": user_id,
                "classification": None
            }
        )

        for complaint in unclassified:
            try:
                complain_series = pd.Series([complaint.complaint])
                predicted_result = int(ml_pipeline.predict(complain_series)[0])
                category = complain_map[predicted_result]
                # complaint.classification = category

                sentiment_result = sentiment_classifier(complaint.complaint)[0]
                # complaint.sentiment = sentiment_result["label"]
                # complaint.sentimentScore = sentiment_result["score"]

                await prisma.complaint.update(
                    where={"id": complaint.id},
                    data={
                        "classification": category,
                        "sentiment": sentiment_result["label"],
                        "sentimentScore": float(sentiment_result["score"])
                    }
                )

                # db.session.commit()

            except Exception as e:
                print(f"Error classifying complaint ID {complaint.id}: {e}")

    except Exception as e:
        print(f"Error accessing complaints for user {user_id}: {e}")

        # pass