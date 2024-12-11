from fastapi import FastAPI
from pydantic import BaseModel
from .helpers import get_yt_comments, get_reddit_post_comments
from .model_preprocessing import preprocessing
from model.w2v import w2v_model, kmeans_clusters
from sklearn.cluster import KMeans
from .bigram_trigram import get_ngrams, generate_bigrams, count_vectorizer_bigram
import numpy as np
import pandas as pd

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
    dup_comments = comments
    comments = preprocessing(comments, data['platform'])
    print(f"comments shape : {len(dup_comments)}")
    # comments_bigram = generate_bigrams(dup_comments)
    comments_bigram = count_vectorizer_bigram(comments)
    print(f"bigrammed_commenta : {comments_bigram}")
    print(f"bigrammed shape : {comments_bigram.shape}")
    clusterer = KMeans(n_clusters=2, random_state=42, max_iter=1000)
    clusterer.fit(comments_bigram)
    pred = pd.DataFrame(clusterer.labels_).to_numpy()
    dup_comments = pd.DataFrame(dup_comments, columns=["comment"])
    dup_comments.drop(index=dup_comments.shape[0]-1, inplace=True)
    print(f"comments shape : {dup_comments.shape}")
    dup_comments = dup_comments["comment"].to_list()
    positive_comments = []
    for i in range(pred.shape[0]):
        if pred[i] == 1:
          positive_comments.append(dup_comments[i])
    print(len(positive_comments))  
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
