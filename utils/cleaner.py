import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    # handeling the null value
    if pd.isna(text):
        return ""
    
    text = re.sub(r'@\w+' , '', text) # removing mentions (@)
    text = re.sub(r'\d+','',text) # removing numbers
    text = re.sub(r"[^\w\s]",'',text) # removing punctuation 
    
    # removing special characters and punctuation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
    # cleaned_text = text.translate(str.maketrans('','',string.punctuation))
    
    # cleaned_text.lower()
        
    
    #tokeniztion
    tokens  = word_tokenize(text)
    
    # lemmentization (converting words to their root form)                
    cleaned_tokens= [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words] 
    cleaned_token = [word.lower() for word in cleaned_tokens ]
    
    return ' '.join(cleaned_token)
        