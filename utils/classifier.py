import pandas as pd
from website.app.pages.api.user.models import db, Complaint
from utils.ml_pipeline import pipeline, complain_map


def classify_user_complaints(user_id):
    """Classify only the current logged-in user's unclassified complaints."""
    print(f"Classifying complaints for user {user_id}")

    from website.app.pages.api.user.server import app as flask_app
    with flask_app.app_context():
        unclassified = Complaint.query.filter_by(user_id=user_id, classification=None).all()
        for complaint in unclassified:
            try:
                complain_series = pd.Series([complaint.complaint])
        
                predicted_result = int(pipeline.predict(complain_series)[0])  # Convert np.int64 to Python int  
                category = complain_map[predicted_result]
                complaint.classification = category
                db.session.commit()
            except Exception as e:
                print(f"Error classifying complaint ID {complaint.id}: {e}")
