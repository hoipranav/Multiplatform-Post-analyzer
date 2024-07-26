from fastapi import FastAPI
from pydantic import BaseModel

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
    return data['url']