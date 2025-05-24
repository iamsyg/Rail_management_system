# import pandas as pd
# import numpy as np
# import re
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer

# # Download necessary NLTK resources
# #nltk.download('stopwords')
# #nltk.download('punkt')
# #nltk.download('wordnet')

# stop_words = set(stopwords.words('english'))
# lemmatizer = WordNetLemmatizer()

# def clean_text(text):
#     # handeling the null value
#     if pd.isna(text):
#         return ""
    
#     text = re.sub(r'@\w+' , '', text) # removing mentions (@)
#     text = re.sub(r'\d+','',text) # removing numbers
#     text = re.sub(r"[^\w\s]",'',text) # removing punctuation 
    
#     # removing special characters and punctuation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
#     # cleaned_text = text.translate(str.maketrans('','',string.punctuation))
    
#     # cleaned_text.lower()
        
    
#     #tokeniztion
#     tokens  = word_tokenize(text)
    
#     # lemmentization (converting words to their root form)                
#     cleaned_tokens= [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words] 
#     cleaned_token = [word.lower() for word in cleaned_tokens ]
    
#     return ' '.join(cleaned_token)
        


import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources with error handling
def ensure_nltk_resources():
    resources = [
        ('stopwords', 'corpora/stopwords'),
        ('punkt', 'tokenizers/punkt'),
        ('wordnet', 'corpora/wordnet')
    ]
    
    for resource_name, resource_path in resources:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            print(f"Downloading {resource_name}...")
            nltk.download(resource_name, quiet=True)

# Ensure resources are available
ensure_nltk_resources()

# Initialize global variables after ensuring resources are available
try:
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
except LookupError as e:
    print(f"Error loading NLTK resources: {e}")
    # Fallback to basic stopwords if NLTK fails
    stop_words = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 
        'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
        'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
        'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
        'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
        'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
        'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after', 'above', 
        'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
        'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 
        'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 
        'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
        'can', 'will', 'just', 'should', 'now'
    }
    lemmatizer = None

def clean_text(text):
    # handling the null value
    if pd.isna(text):
        return ""
    
    text = re.sub(r'@\w+', '', text)  # removing mentions (@)
    text = re.sub(r'\d+', '', text)  # removing numbers
    text = re.sub(r"[^\w\s]", '', text)  # removing punctuation 
    
    # tokenization with fallback
    try:
        tokens = word_tokenize(text)
    except LookupError:
        # Fallback tokenization if NLTK punkt is not available
        tokens = text.split()
    
    # lemmatization (converting words to their root form) with fallback               
    if lemmatizer:
        cleaned_tokens = [lemmatizer.lemmatize(word) for word in tokens if word.lower() not in stop_words]
    else:
        # Fallback without lemmatization
        cleaned_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    cleaned_token = [word.lower() for word in cleaned_tokens]
    
    return ' '.join(cleaned_token)