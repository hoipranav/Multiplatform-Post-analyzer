from fastapi import FastAPI
from pydantic import BaseModel
from platform_api import get_yt_comments, get_x_comments, get_linkedIn_comments

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
    print(videoid)
    while True:
        comments, pageToken = get_yt_comments(videoid, token)
        token = pageToken
        if pageToken == "KeyError":
            break

    return comments

@app.post('/scrape/x')
async def scrape_x(data: X_params):
    data = dict(data)
    content = data['url']
    tweets = get_x_comments(content)

    return tweets

@app.post('/scrape/linkedIn')
async def scrape_linkedIn(data: LinkedIn_params):
    data = dict(data)
    postid = data['url'].split('-')[4]
    comments = get_linkedIn_comments(postid)

    return comments
