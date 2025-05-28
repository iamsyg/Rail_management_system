import warnings
warnings.filterwarnings("ignore")
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from utils.cleaner import clean_text

with open('./models/classiffication_model.pkl', 'rb') as file:
    classification_model = pickle.load(file)

with open('./models/tfidf_vecterizor.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Preprocessing step
text_cleaner = FunctionTransformer(lambda x: x.apply(clean_text), validate=False)

# Create the ML pipeline
pipeline = Pipeline([
    ('cleaner', text_cleaner),
    ('vectorizer', vectorizer),
    ('classifier', classification_model)
])

# Class labels
complain_map = {
    0: 'Cleanliness',
    1: 'Others',
    2: 'Medical issues',
    3: 'Food Services',
    4: 'Train Delay',
    5: 'Ticket issues',
    6: 'No use',
    7: 'No use'
}