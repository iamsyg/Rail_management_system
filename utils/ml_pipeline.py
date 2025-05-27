# import warnings
# warnings.filterwarnings("ignore")
# import pickle
# import pandas as pd
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import FunctionTransformer
# from utils.cleaner import clean_text

# with open('./models/classiffication_model.pkl', 'rb') as file:
#     classification_model = pickle.load(file)

# with open('./models/tfidf_vecterizor.pkl', 'rb') as file:
#     vectorizer = pickle.load(file)

# # Preprocessing step
# text_cleaner = FunctionTransformer(lambda x: x.apply(clean_text), validate=False)

# # Create the ML pipeline
# pipeline = Pipeline([
#     ('cleaner', text_cleaner),
#     ('vectorizer', vectorizer),
#     ('classifier', classification_model)
# ])

# # Class labels
# complain_map = {
#     0: 'Cleanliness',
#     1: 'Others',
#     2: 'Medical issues',
#     3: 'Food Services',
#     4: 'Train Delay',
#     5: 'Ticket issues',
#     6: 'No use',
#     7: 'No use'
# }



import warnings
warnings.filterwarnings("ignore")
import pickle
import pandas as pd
import gc
import os
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from utils.cleaner import clean_text

# Global variables for lazy loading
_classification_model = None
_vectorizer = None
_pipeline = None

# Class labels (this is lightweight, can be loaded immediately)
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

def load_classification_model():
    """Lazy load the classification model"""
    global _classification_model
    
    if _classification_model is None:
        try:
            model_path = './models/classiffication_model.pkl'
            print(f"Loading classification model from {model_path}")
            
            with open(model_path, 'rb') as file:
                _classification_model = pickle.load(file)
            
            print("Classification model loaded successfully")
            
        except FileNotFoundError:
            print(f"Model file not found: {model_path}")
            raise
        except Exception as e:
            print(f"Error loading classification model: {e}")
            raise
    
    return _classification_model

def load_vectorizer():
    """Lazy load the TF-IDF vectorizer"""
    global _vectorizer
    
    if _vectorizer is None:
        try:
            vectorizer_path = './models/tfidf_vecterizor.pkl'
            print(f"Loading vectorizer from {vectorizer_path}")
            
            with open(vectorizer_path, 'rb') as file:
                _vectorizer = pickle.load(file)
            
            print("Vectorizer loaded successfully")
            
        except FileNotFoundError:
            print(f"Vectorizer file not found: {vectorizer_path}")
            raise
        except Exception as e:
            print(f"Error loading vectorizer: {e}")
            raise
    
    return _vectorizer

def get_pipeline():
    """Lazy load and create the ML pipeline"""
    global _pipeline
    
    if _pipeline is None:
        try:
            print("Creating ML pipeline...")
            
            # Load components
            classification_model = load_classification_model()
            vectorizer = load_vectorizer()
            
            # Preprocessing step
            text_cleaner = FunctionTransformer(
                lambda x: x.apply(clean_text), 
                validate=False
            )
            
            # Create the ML pipeline
            _pipeline = Pipeline([
                ('cleaner', text_cleaner),
                ('vectorizer', vectorizer),
                ('classifier', classification_model)
            ])
            
            print("ML pipeline created successfully")
            
            # Force garbage collection after loading
            gc.collect()
            
        except Exception as e:
            print(f"Error creating ML pipeline: {e}")
            raise
    
    return _pipeline

# Create a wrapper class for the pipeline to maintain compatibility
class LazyPipeline:
    def predict(self, X):
        """Predict using the lazy-loaded pipeline"""
        pipeline = get_pipeline()
        return pipeline.predict(X)
    
    def predict_proba(self, X):
        """Predict probabilities using the lazy-loaded pipeline"""
        pipeline = get_pipeline()
        return pipeline.predict_proba(X)
    
    def transform(self, X):
        """Transform data using the lazy-loaded pipeline"""
        pipeline = get_pipeline()
        return pipeline.transform(X)

# Create the lazy pipeline instance
pipeline = LazyPipeline()

def cleanup_models():
    """Clean up loaded models to free memory"""
    global _classification_model, _vectorizer, _pipeline
    
    if _classification_model is not None:
        del _classification_model
        _classification_model = None
    
    if _vectorizer is not None:
        del _vectorizer
        _vectorizer = None
    
    if _pipeline is not None:
        del _pipeline
        _pipeline = None
    
    gc.collect()
    print("ML models cleaned up")

def get_model_info():
    """Get information about loaded models"""
    info = {
        'classification_model_loaded': _classification_model is not None,
        'vectorizer_loaded': _vectorizer is not None,
        'pipeline_created': _pipeline is not None
    }
    return info