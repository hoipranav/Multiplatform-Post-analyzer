import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import html
import numpy as np
import pandas as pd
import joblib

lemmatizer = WordNetLemmatizer()

def create_df(file):
    comments_df = pd.DataFrame(file, columns=['comment'])
    return comments_df

def make_lowercase(file):
    for i in range(len(file)):
        file.iloc[i] = file.iloc[i].values[0].strip().lower()   
    return file

def remove_punctuation(file):
    punctuation_pattern = r'[^\w\s]'
    for i in range(file.shape[0]):
        file.iloc[i] = re.sub(punctuation_pattern, '', file.iloc[i].values[0].strip())
    return file

def remove_stopwords(file):
    stop_words = set(stopwords.words('english'))
    for i in range(len(file)):
        text = file.iloc[i].values[0].split()
        filtered_words = [word for word in text if word not in stop_words]
        filtered_text_sentence = ' '.join(filtered_words)
        file.iloc[i] = filtered_text_sentence
    return file

def remove_html(file):
    html_tags_pattern = r'<.*?>'
    for i in range(file.shape[0]):
        text = file.iloc[i].values[0]
        file.iloc[i] = re.sub(html_tags_pattern, '', text)
    return file

def unescape_html(file):
    for i in range(file.shape[0]):
        text = file.iloc[i].values[0]
        file.iloc[i] = html.unescape(text)
    return file

def remove_url(file):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    for i in range(len(file)):
        text = file.iloc[i].values[0]
        file.iloc[i] = url_pattern.sub(r'', text)
    return file

def lemmatize_text(file):
    for i in range(file.shape[0]):
        text = file.iloc[i].values[0].split()
        lemmatized_words = [lemmatizer.lemmatize(word, pos='v') for word in text]
        lemmatized_sentence = ' '.join(lemmatized_words)
        file.iloc[i] = lemmatized_sentence
    return file

def detect_lang(file):
    index_list = []
    model = joblib.load('./model/language_detector.pkl')
    cv = joblib.load('./model/cv.pkl')
    for i in range(file.shape[0]):
        text = file.iloc[i].values
        text_cv = cv.transform(text)
        if model.predict(text_cv)[0] == 3:
            file.iloc[i] = text
        if model.predict(text_cv)[0] != 3:
            index_list.append(i)
    file.drop(index=index_list, inplace=True)
    return file

def preprocessing(comments: list, platform: str):
    comments = create_df(comments)
    comments = remove_html(comments)
    comments = unescape_html(comments)
    comments = make_lowercase(comments)
    comments = remove_punctuation(comments)
    comments = remove_url(comments)
    comments = remove_stopwords(comments)
    comments = lemmatize_text(comments)
    comments = detect_lang(comments)
    return comments 