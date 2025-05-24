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

# Initialize variables that will be set after downloading resources
stop_words = None
lemmatizer = None

def ensure_nltk_resources():
    """Download NLTK resources if not available"""
    global stop_words, lemmatizer
    
    # Set NLTK data path to ensure it's writable on Render
    import os
    nltk_data_dir = '/tmp/nltk_data'
    if not os.path.exists(nltk_data_dir):
        os.makedirs(nltk_data_dir)
    nltk.data.path.append(nltk_data_dir)
    
    resources_to_download = ['stopwords', 'punkt', 'wordnet']
    
    for resource in resources_to_download:
        try:
            # Try to access the resource to see if it exists
            if resource == 'stopwords':
                from nltk.corpus import stopwords
                stopwords.words('english')
            elif resource == 'punkt':
                from nltk.tokenize import word_tokenize
                word_tokenize("test")
            elif resource == 'wordnet':
                from nltk.stem import WordNetLemmatizer
                WordNetLemmatizer()
        except LookupError:
            print(f"Downloading NLTK {resource}...")
            try:
                nltk.download(resource, download_dir=nltk_data_dir, quiet=True)
                print(f"Successfully downloaded {resource}")
            except Exception as e:
                print(f"Failed to download {resource}: {e}")
    
    # Initialize global variables after download
    try:
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        print("NLTK resources initialized successfully")
    except Exception as e:
        print(f"Failed to initialize NLTK resources: {e}")
        # Fallback to basic stopwords
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

# Call the function to ensure resources are available
ensure_nltk_resources()

def clean_text(text):
    # handling the null value
    if pd.isna(text):
        return ""
    
    text = re.sub(r'@\w+', '', text)  # removing mentions (@)
    text = re.sub(r'\d+', '', text)  # removing numbers
    text = re.sub(r"[^\w\s]", '', text)  # removing punctuation 
    
    # tokenization with fallback
    try:
        from nltk.tokenize import word_tokenize
        tokens = word_tokenize(text)
    except (LookupError, ImportError):
        # Fallback tokenization if NLTK punkt is not available
        tokens = text.split()
    
    # lemmatization (converting words to their root form) with fallback               
    if lemmatizer:
        try:
            cleaned_tokens = [lemmatizer.lemmatize(word) for word in tokens if word.lower() not in stop_words]
        except:
            # Fallback without lemmatization
            cleaned_tokens = [word for word in tokens if word.lower() not in stop_words]
    else:
        # Fallback without lemmatization
        cleaned_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    cleaned_token = [word.lower() for word in cleaned_tokens]
    
    return ' '.join(cleaned_token)