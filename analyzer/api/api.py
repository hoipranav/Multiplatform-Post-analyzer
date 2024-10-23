from fastapi import FastAPI
from pydantic import BaseModel
from .helpers import get_yt_comments, get_reddit_post_comments
from .model_preprocessing import preprocessing
from model.w2v import w2v_model, kmeans_clusters
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from .tfdif_replace import create_tfidf_dictionary, replace_tfidf_words
class Youtube_params(BaseModel):
    url: str
    platform: str

class Reddit_params(BaseModel):
    url: str
    platform: str


app = FastAPI()


@app.get('/')
async def root():
    """
    Welcome message for the API
    """
    return {'message': "Welcome to the Platform-analyzer API"}


@app.post('/scrape/youtube')
async def scrape_yt(data: Youtube_params):
    """
    Scrape comments from a youtube video

    Args:
        data (Youtube_params): The url of the video and the platform

    Returns:
        list: The list of comments
    """
    token = ""
    data = dict(data)
    videoid = data['url'].split('=')[1]
    while True:
        comments, pageToken = get_yt_comments(videoid, token)
        token = pageToken
        if pageToken == "KeyError":
            break
    comments = preprocessing(comments, data['platform'])
    dup_comments = pd.DataFrame(comments)
    print(dup_comments)
    w2v_model(comments)
    scores = kmeans_clusters(comments)
    tfidf = TfidfVectorizer(tokenizer=lambda y: y.split(), norm=None)
    tfidf.fit(dup_comments.comment)
    features = pd.DataFrame(tfidf.get_feature_names_out())
    print(f"features : {features}")
    transformed = tfidf.transform(dup_comments)
    print(f"transformed shape ; {type(transformed.shape)}")
    replaced_tf_scores = dup_comments.apply(lambda x: replace_tfidf_words(x, transformed, features), axis=1)
    print(f"scores : {scores} \n replaced_tfidf_scores : {replaced_tf_scores}")
    return ["hi"]


@app.post('/scrape/reddit')
async def scrape_reddit(data: Reddit_params):
    """
    Scrape comments from a reddit post

    Args:
        data (Reddit_params): The url of the post and the platform

    Returns:
        list: The list of comments
    """
    data = dict(data)
    comments = get_reddit_post_comments(data['url'])
    comments = preprocessing(comments, data['platform'])
    return comments
