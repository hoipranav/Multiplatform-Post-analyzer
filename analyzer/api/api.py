from fastapi import FastAPI
from pydantic import BaseModel
from .helpers import get_yt_comments, get_reddit_post_comments
from .model_preprocessing import preprocessing
from model.w2v import w2v_model, kmeans_clusters
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from .tfdif_replace import replace_tfidf_words, replace_sentiment_words
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
    dup_comments = comments
    print(f"comments shape : {dup_comments.shape}")
    w2v_model(comments)
    scores = kmeans_clusters(comments)
    tfidf = TfidfVectorizer(tokenizer=lambda y: y.split(), norm=None)
    tfidf.fit(comments.comment)
    features = tfidf.get_feature_names_out()
    features_transformed = features[:, np.newaxis]
    print(f"features : {features_transformed.shape}")
    transformed = tfidf.transform(comments.comment)
    print(f"transformed shape ; {transformed.shape}")
    replaced_tf_scores = dup_comments.apply(lambda x: replace_tfidf_words(x, transformed, features_transformed), axis=1)
    print(replaced_tf_scores.shape)
    replaced_closeness_scores = comments.comment.apply(lambda x: list(map(lambda y: replace_sentiment_words(y, scores), x.split())))
    print(f"closeness score:{replaced_closeness_scores.shape}")
    replacement_df = pd.DataFrame(data=[replaced_closeness_scores, replaced_tf_scores, comments.comment]).T
    replacement_df.columns = ['sentiment_coeff', 'tfidf_score', 'sentence']
    replacement_df['sentiment_rate'] = replacement_df.apply(lambda x:np.array(x.loc['sentiment_coeff']) @ np.array(x.loc['tfidf_score']), axis=1)
    replacement_df['prediction'] = (replacement_df.sentiment_rate>0).astype('int8')
    print(f"replacement_df: {replacement_df}")
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
