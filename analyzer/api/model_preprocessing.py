import re
import html
import numpy as np
import pandas as pd
import joblib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def create_df(file):
    """
    Creates a DataFrame from a given file.

    Args:
        file (list): A list of comments

    Returns:
        pd.DataFrame: A DataFrame with a single column 'comment'
    """
    comments_df = pd.DataFrame(file, columns=['comment'])
    return comments_df


def make_lowercase(file):
    """
    Convert all the comments in the given DataFrame to lowercase.

    Args:
        file (pd.DataFrame): A DataFrame with a single column 'comment'

    Returns:
        pd.DataFrame: The DataFrame with all comments converted to lowercase
    """
    for i in range(len(file)):
        file.iloc[i] = file.iloc[i].values[0].strip().lower()
    return file


def remove_punctuation(file):
    """
    Remove punctuation from all comments in the given DataFrame.

    Args:
        file (pd.DataFrame): A DataFrame with a single column 'comment'

    Returns:
        pd.DataFrame: The DataFrame with all comments stripped of punctuation
    """
    punctuation_pattern = r'[^\w\s]'
    for i in range(file.shape[0]):
        file.iloc[i] = re.sub(punctuation_pattern, '', file.iloc[i].values[0].strip())
    return file


def remove_stopwords(file):
    """
    Remove stopwords from all comments in the given DataFrame.

    Args:
        file (pd.DataFrame): A DataFrame with a single column 'comment'

    Returns:
        pd.DataFrame: The DataFrame with all comments stripped of stopwords
    """
    stop_words = set(stopwords.words('english'))
    for i in range(len(file)):
        text = file.iloc[i].values[0].split()
        filtered_words = [word for word in text if word not in stop_words]
        filtered_text_sentence = ' '.join(filtered_words)
        file.iloc[i] = filtered_text_sentence
    return file


def remove_html(file):
    """
    Remove HTML tags from all comments in the given DataFrame.

    Args:
        file (pd.DataFrame): A DataFrame with a single column 'comment'

    Returns:
        pd.DataFrame: The DataFrame with all comments stripped of HTML tags
    """
    html_tags_pattern = r'<.*?>'
    for i in range(file.shape[0]):
        text = file.iloc[i].values[0]
        file.iloc[i] = re.sub(html_tags_pattern, '', text)
    return file


def unescape_html(file):
    """
    Unescape HTML entities in all comments in the given DataFrame.

    Args:
        file (pd.DataFrame): A DataFrame with a single column 'comment'

    Returns:
        pd.DataFrame: The DataFrame with all comments unescaped of HTML entities
    """
    for i in range(file.shape[0]):
        text = file.iloc[i].values[0]
        file.iloc[i] = html.unescape(text)
    return file


def remove_url(file):
    """
    Remove URLs from all comments in the given DataFrame.

    Args:
        file (pd.DataFrame): A DataFrame with a single column 'comment'

    Returns:
        pd.DataFrame: The DataFrame with all comments stripped of URLs
    """
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    for i in range(len(file)):
        text = file.iloc[i].values[0]
        file.iloc[i] = url_pattern.sub(r'', text)
    return file


def lemmatize_text(file):
    """
    Lemmatize all words in all comments in the given DataFrame.

    Args:
        file (pd.DataFrame): A DataFrame with a single column 'comment'

    Returns:
        pd.DataFrame: The DataFrame with all words lemmatized
    """
    for i in range(file.shape[0]):
        text = file.iloc[i].values[0].split()
        lemmatized_words = [lemmatizer.lemmatize(word, pos='v') for word in text]
        lemmatized_sentence = ' '.join(lemmatized_words)
        file.iloc[i] = lemmatized_sentence
    return file


def detect_lang(file):
    """
    Detect the language of all comments in the given DataFrame and drop the
    comments that are not in English.

    Args:
        file (pd.DataFrame): A DataFrame with a single column 'comment'

    Returns:
        pd.DataFrame: The DataFrame with all comments in English
    """
    index_list = []
    model = joblib.load('./analyzer/model/language_detector.pkl')
    cv = joblib.load('./analyzer/model/cv.pkl')
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
    """
    Preprocesses the comments data by:

    1. Removing HTML tags
    2. Unescaping HTML entities
    3. Converting all text to lowercase
    4. Removing punctuation
    5. Removing URLs
    6. Removing stopwords
    7. Lemmatizing words
    8. Detecting the language of the comments and dropping the comments that are not in English

    Args:
        comments (list): A list of comments
        platform (str): The platform from which the comments come (Youtube or Reddit)

    Returns:
        pd.DataFrame: The preprocessed DataFrame with a single column 'comment'
    """
    comments = create_df(comments)
    comments = remove_html(comments)
    comments = unescape_html(comments)
    comments = make_lowercase(comments)
    comments = remove_punctuation(comments)
    comments = remove_url(comments)
    comments = remove_stopwords(comments)
    comments = lemmatize_text(comments)
    comments = detect_lang(comments)
    comments.dropna().reset_index(drop=True)
    return comments
