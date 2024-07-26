from fastapi import FastAPI
from pydantic import BaseModel
from data import scrape_platform

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
    comments = scrape_platform(data['url'])
    return comments