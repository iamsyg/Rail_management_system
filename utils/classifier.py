# import pandas as pd
# # from website.app.pages.api.user.models import db, Complaint
# from utils.ml_pipeline import pipeline as ml_pipeline, complain_map
# from transformers import pipeline as hf_pipeline

# from database.lib.prisma import prisma

# # Sentiment classifier
# sentiment_classifier = hf_pipeline("sentiment-analysis", framework="tf", model="distilbert-base-uncased-finetuned-sst-2-english")

# async def classify_user_complaints(user_id):
#     """Classify only the current logged-in user's unclassified complaints."""
#     print(f"Classifying complaints for user {user_id}")

#     try:
#         unclassified = await prisma.complaint.find_many(
#             where={
#                 "user_id": user_id,
#                 "classification": None
#             }
#         )

#         for complaint in unclassified:
#             try:
#                 complain_series = pd.Series([complaint.complaint])
#                 predicted_result = int(ml_pipeline.predict(complain_series)[0])
#                 category = complain_map[predicted_result]
#                 # complaint.classification = category

#                 sentiment_result = sentiment_classifier(complaint.complaint)[0]
#                 # complaint.sentiment = sentiment_result["label"]
#                 # complaint.sentimentScore = sentiment_result["score"]

#                 await prisma.complaint.update(
#                     where={"id": complaint.id},
#                     data={
#                         "classification": category,
#                         "sentiment": sentiment_result["label"],
#                         "sentimentScore": float(sentiment_result["score"])
#                     }
#                 )

#                 # db.session.commit()

#             except Exception as e:
#                 print(f"Error classifying complaint ID {complaint.id}: {e}")

#     except Exception as e:
#         print(f"Error accessing complaints for user {user_id}: {e}")

#         # pass




import pandas as pd
import gc
import os
from utils.ml_pipeline import pipeline as ml_pipeline, complain_map
from database.lib.prisma import prisma

# Global variables for lazy loading
_sentiment_classifier = None

def get_sentiment_classifier():
    """Lazy load the sentiment classifier to save memory"""
    global _sentiment_classifier
    
    if _sentiment_classifier is None:
        try:
            # Import transformers only when needed
            from transformers import pipeline as hf_pipeline
            
            # Set environment variables to optimize memory usage
            os.environ['TOKENIZERS_PARALLELISM'] = 'false'
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            
            print("Loading sentiment classifier...")
            _sentiment_classifier = hf_pipeline(
                "sentiment-analysis", 
                framework="tf", 
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1,  # Force CPU usage
                model_kwargs={
                    "low_cpu_mem_usage": True,
                    "torch_dtype": "auto"
                }
            )
            print("Sentiment classifier loaded successfully")
            
            # Force garbage collection after loading
            gc.collect()
            
        except Exception as e:
            print(f"Error loading sentiment classifier: {e}")
            # Fallback to simple sentiment analysis
            _sentiment_classifier = None
    
    return _sentiment_classifier

def simple_sentiment_analysis(text):
    """Fallback sentiment analysis without transformers"""
    positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'perfect', 'love', 'best', 'awesome'}
    negative_words = {'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'disgusting', 'useless', 'disappointing', 'pathetic'}
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return {"label": "POSITIVE", "score": 0.7}
    elif negative_count > positive_count:
        return {"label": "NEGATIVE", "score": 0.7}
    else:
        return {"label": "NEUTRAL", "score": 0.5}

async def classify_user_complaints(user_id):
    """Classify only the current logged-in user's unclassified complaints."""
    print(f"Classifying complaints for user {user_id}")

    try:
        # Get unclassified complaints in batches to reduce memory usage
        batch_size = 10  # Process in smaller batches
        skip = 0
        
        while True:
            unclassified = await prisma.complaint.find_many(
                where={
                    "user_id": user_id,
                    "classification": None
                },
                skip=skip,
                take=batch_size
            )
            
            if not unclassified:
                break
                
            print(f"Processing batch of {len(unclassified)} complaints")
            
            # Get sentiment classifier (lazy loaded)
            sentiment_classifier = get_sentiment_classifier()
            
            for complaint in unclassified:
                try:
                    # Classification using ML pipeline
                    complain_series = pd.Series([complaint.complaint])
                    predicted_result = int(ml_pipeline.predict(complain_series)[0])
                    category = complain_map[predicted_result]

                    # Sentiment analysis with fallback
                    if sentiment_classifier is not None:
                        try:
                            sentiment_result = sentiment_classifier(complaint.complaint)[0]
                        except Exception as e:
                            print(f"Transformers sentiment failed, using fallback: {e}")
                            sentiment_result = simple_sentiment_analysis(complaint.complaint)
                    else:
                        sentiment_result = simple_sentiment_analysis(complaint.complaint)

                    # Update database
                    await prisma.complaint.update(
                        where={"id": complaint.id},
                        data={
                            "classification": category,
                            "sentiment": sentiment_result["label"],
                            "sentimentScore": float(sentiment_result["score"])
                        }
                    )

                    print(f"Classified complaint {complaint.id}: {category}, {sentiment_result['label']}")

                except Exception as e:
                    print(f"Error classifying complaint ID {complaint.id}: {e}")
                    # Continue with next complaint instead of failing
                    continue
            
            # Force garbage collection after each batch
            gc.collect()
            skip += batch_size

        print(f"Completed classification for user {user_id}")

    except Exception as e:
        print(f"Error accessing complaints for user {user_id}: {e}")

def cleanup_models():
    """Clean up loaded models to free memory"""
    global _sentiment_classifier
    if _sentiment_classifier is not None:
        del _sentiment_classifier
        _sentiment_classifier = None
        gc.collect()
        print("Models cleaned up")