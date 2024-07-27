from fastapi import FastAPI
from pydantic import BaseModel
from yt_api import get_top_level_comments

class Data(BaseModel):
    url: str
    platform: str

app = FastAPI()

@app.get('/')
async def root():
    return {'message': "Welcome to the Multiplatform-post-analyzer API"}

@app.post('/scrape')
async def scrape(data: Data):
    data = dict(data)
    videoid = data['url'].split('=')[1]
    comments = get_top_level_comments(videoid=videoid)
    return comments
