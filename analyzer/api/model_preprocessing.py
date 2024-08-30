import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import html


lemmatizer = WordNetLemmatizer()

def make_lowercase(file):
    for i in range(len(file)):
        file[i] = file[i].strip().lower()   
    return file

def remove_punctuation(file):
    punctuation_pattern = r'[^\w\s]'
    for i in range(len(file)):
        file[i] = re.sub(punctuation_pattern, '', file[i].strip())
    return file

def remove_stopwords(file):
    stop_words = set(stopwords.words('english'))
    for i in range(len(file)):
        text = file[i].split()
        filtered_words = [word for word in text if word not in stop_words]
        filtered_text_sentence = ' '.join(filtered_words)
        file[i] = filtered_text_sentence
    return file

def remove_html(file):
    html_tags_pattern = r'<.*?>'
    for i in range(len(file)):
        text = file[i]
        file[i] = re.sub(html_tags_pattern, '', text)
    return file

def unescape_html(file):
    for i in range(len(file)):
        text = file[i]
        file[i] = html.unescape(text)
    return file

def remove_url(file):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    for i in range(len(file)):
        text = file[i]
        file[i] = url_pattern.sub(r'', text)
    return file

def lemmatize_text(file):
    for i in range(len(file)):
        text = file[i].split()
        lemmatized_words = [lemmatizer.lemmatize(word, pos='v') for word in text]
        lemmatized_sentence = ' '.join(lemmatized_words)
        file[i] = lemmatized_sentence
    return file

def preprocessing(comments: list, platform: str):
    comments = remove_html(comments)
    comments = unescape_html(comments)
    comments = make_lowercase(comments)
    comments = remove_punctuation(comments)
    comments = remove_url(comments)
    comments = remove_stopwords(comments)
    comments = lemmatize_text(comments)
    return comments