from fastapi import FastAPI
from pydantic import BaseModel
from analyzer.api.helpers import get_yt_comments


class Youtube_params(BaseModel):
    url: str
    platform: str

class X_params(BaseModel):
    content: str
    platform: str

class LinkedIn_params(BaseModel):
    url: str
    platform: str

app = FastAPI()


@app.get('/')
async def root():
    return {'message': "Welcome to the Multiplatform-post-analyzer API"}


@app.post('/scrape/youtube')
async def scrape_yt(data: Youtube_params):
    token = ""
    data = dict(data)
    videoid = data['url'].split('=')[1]
    while True:
        comments, pageToken = get_yt_comments(videoid, token)
        token = pageToken
        if pageToken == "KeyError":
            break

    return comments
