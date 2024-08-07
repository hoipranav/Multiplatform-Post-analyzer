import googleapiclient.discovery
# import snscrape.modules.twitter as sntwitter
import requests
import os

comments_list = []
iter = 0

def get_yt_comments(videoid: str, pageToken: str):
    '''Uses Youtube Data API to fetch the comments from a Particular video by using the video id as parameter'''
    global iter, comments_list
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ["yt_api_key"]

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )
    if iter == 0:
        comments_list = []
        request = youtube.commentThreads().list(
            part = "snippet",
            videoId = videoid,
            maxResults = 100,
        )
        iter += 1
    if iter != 0:
        request = youtube.commentThreads().list(
            part = "snippet",
            videoId = videoid,
            maxResults = 100,
            pageToken = pageToken
        )
    response = request.execute()
    
    for i in range(100):
        try:
            comments_list.append(
                response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            )
        except IndexError:
            iter = 0
            return comments_list, "KeyError"

    return comments_list, response["nextPageToken"]

def get_x_comments(content: str):
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper("").get_items()):
        if i > 10:
            break
        comments_list.append(tweet.conversationId)
    
    return comments_list

def get_linkedIn_comments(urn: str) -> list:
    url = "https://linkedin-data-api.p.rapidapi.com/get-profile-posts-comments"
    querystring = {"urn":urn,"sort":"mostRelevant"}
    headers = {
        "x-rapidapi-key": os.environ["x_rapidapi_key"],
        "x-rapidapi-host": os.environ["x_rapidapi_host"]
    }
    response = requests.get(url, headers=headers, params=querystring).json()
    response = response["data"]
    comments_list = [i["text"] for i in response]

    return comments_list
