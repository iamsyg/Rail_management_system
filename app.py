import threading
import subprocess
from flask import Flask, request
from website.app.pages.api.user.server import app as flask_app , db # Import Flask app
from website.app.pages.api.user.auth import get_logged_in_user  
import requests

from website.app.pages.api.user.models import Complaint,User
from flask_jwt_extended import jwt_required, get_jwt_identity

# functions and imports for machine learing pipeline
from utils.cleaner import clean_text
import pickle
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

# def get_logged_in_user():
#     try:
#         access_token = request.cookies.get("access_token")
#         response = requests.get("http://localhost:8080/pages/api/user/profile", 
#                                 cookies={"access_token": access_token})

#         if response.status_code == 200:
#             user_data = response.json()["user"]
#             print("✅ Logged-in user details:", user_data)
#             return user_data
#         else:
#             print("❌ Failed to get user:", response.json())
#     except Exception as e:
#         print("❌ Error fetching user:", e)
#     return None

# user_data = get_logged_in_user()
# print(user_data["name"])



#importing models
with open('./models/classiffication_model.pkl','rb') as file :
    classification_model = pickle.load(file)
with open ('./models/tfidf_vecterizor.pkl','rb') as file:
    vectorizor = pickle.load(file)

# transforming the function to use it in the pipeline
text_cleaner = FunctionTransformer(lambda x: x.apply(clean_text), validate=False)

# crreating pipeline
pipeline = Pipeline([
    ('cleaner',text_cleaner),
    ('vectorizer',vectorizor),
    ('classifier',classification_model)
])

complain_map = {'0': 'Cleanliness',
1: 'Others',
2: 'Medical issues',
3: 'Food Services',
4: 'Train Delay',
5: 'Ticket issues',
6:  'No use',
7:  'No use'
}

def run_nextjs():
    try:
        # `shell=True` is important on Windows to run npm correctly
        subprocess.call("npm run dev", cwd="website", shell=True)
    except FileNotFoundError as e:
        print("❌ Error launching Next.js app:", e)

app = Flask(__name__)

with flask_app.app_context():
    unclassified_complains = Complaint.query.filter(
        Complaint.classification == None
    ).limit(100).all()
    
    for complaint in unclassified_complains :
        print (f"The processing complaint ID is {complaint.id},Text: {complaint.complaint}")
        complain_series = pd.Series([complaint.complaint])
        
        predicted_result = pipeline.predict(complain_series)  
        category = complain_map[predicted_result[0]]
        print(category)
        
        complaint.classification = category
        
    db.session.commit()
    print("✅ Successfully processed and updated 100 complaints.")

@app.route("/")
def home():
    return "Flask API is running!"

if __name__ == "__main__":
    threading.Thread(target=run_nextjs).start()
    flask_app.run(debug=True, port=8080)
