from utils.cleaner import clean_text
import pickle
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


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

    
input_text = ""

user_df = pd.Series(input_text)
prediction = pipeline.predict(user_df)
    
print("Predicted category:", prediction[0])
