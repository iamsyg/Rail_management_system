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
import ssl

# Handle SSL certificate issues that can occur in some environments
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Function to safely download NLTK resources
def download_nltk_resources():
    resources = ['stopwords', 'punkt', 'wordnet', 'omw-1.4']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else 
                          f'corpora/{resource}' if resource in ['stopwords', 'wordnet', 'omw-1.4'] else resource)
        except LookupError:
            print(f"Downloading {resource}...")
            nltk.download(resource, quiet=True)

# Download necessary NLTK resources
download_nltk_resources()

# Import NLTK components after ensuring resources are available
try:
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
except Exception as e:
    print(f"Error loading NLTK resources: {e}")
    # Fallback: create basic implementations
    stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
                  'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 
                  'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
                  'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
                  'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
                  'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
                  'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after', 
                  'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
                  'further', 'then', 'once'}
    
    def word_tokenize(text):
        return re.findall(r'\b\w+\b', text.lower())
    
    class SimpleWordNetLemmatizer:
        def lemmatize(self, word):
            return word
    
    lemmatizer = SimpleWordNetLemmatizer()

def clean_text(text):
    """
    Clean and preprocess text data for NLP tasks.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned and preprocessed text
    """
    # Handle null values
    if pd.isna(text) or text is None:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Remove mentions (@username)
    text = re.sub(r'@\w+', '', text)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove punctuation and special characters
    text = re.sub(r"[^\w\s]", '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenization
    try:
        tokens = word_tokenize(text)
    except Exception:
        # Fallback tokenization
        tokens = re.findall(r'\b\w+\b', text.lower())
    
    # Remove stopwords and lemmatize
    cleaned_tokens = []
    for word in tokens:
        word_lower = word.lower()
        if word_lower not in stop_words and len(word_lower) > 1:  # Also filter out single characters
            try:
                lemmatized_word = lemmatizer.lemmatize(word_lower)
                cleaned_tokens.append(lemmatized_word)
            except Exception:
                cleaned_tokens.append(word_lower)
    
    return ' '.join(cleaned_tokens)

# Alternative function that doesn't rely on NLTK (backup option)
def clean_text_simple(text):
    """
    Simple text cleaning without NLTK dependencies.
    """
    if pd.isna(text) or text is None:
        return ""
    
    text = str(text).lower()
    
    # Remove mentions, numbers, and punctuation
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r"[^\w\s]", '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Simple stopword removal
    simple_stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
                       'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had'}
    
    words = text.split()
    cleaned_words = [word for word in words if word not in simple_stopwords and len(word) > 1]
    
    return ' '.join(cleaned_words)
        