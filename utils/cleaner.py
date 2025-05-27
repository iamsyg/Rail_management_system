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

# Hardcoded English stopwords (no NLTK dependency)
ENGLISH_STOP_WORDS = {
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
    's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}

def simple_tokenize(text):
    """Simple tokenization without NLTK dependency"""
    # Split by whitespace and remove empty strings
    tokens = text.split()
    # Remove any remaining punctuation from individual tokens
    tokens = [re.sub(r'[^\w]', '', token) for token in tokens]
    # Filter out empty tokens
    return [token for token in tokens if token]

def simple_lemmatize(word):
    """Basic lemmatization rules without NLTK dependency"""
    # Simple plural to singular conversion
    if word.endswith('ies'):
        return word[:-3] + 'y'
    elif word.endswith('es') and len(word) > 3:
        return word[:-2]
    elif word.endswith('s') and len(word) > 3:
        return word[:-1]
    
    # Simple past tense conversion
    if word.endswith('ed') and len(word) > 3:
        return word[:-2]
    
    # Simple -ing conversion
    if word.endswith('ing') and len(word) > 4:
        return word[:-3]
    
    return word

def clean_text(text):
    # handling the null value
    if pd.isna(text):
        return ""
    
    text = re.sub(r'@\w+', '', text)  # removing mentions (@)
    text = re.sub(r'\d+', '', text)  # removing numbers
    text = re.sub(r"[^\w\s]", '', text)  # removing punctuation 
    
    # Convert to lowercase
    text = text.lower()
    
    # tokenization using simple method
    tokens = simple_tokenize(text)
    
    # lemmatization and stopword removal
    cleaned_tokens = [
        simple_lemmatize(word) for word in tokens 
        if word.lower() not in ENGLISH_STOP_WORDS and len(word) > 1
    ]
    
    return ' '.join(cleaned_tokens)