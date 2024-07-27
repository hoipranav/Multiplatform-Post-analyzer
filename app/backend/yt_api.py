import googleapiclient.discovery
import os

def get_top_level_comments(videoid):
    '''Uses Youtube Data API to fetch the comments from a Particular video by using the video id as parameter'''
    comments = []
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ["yt_api_key"]

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )

    request = youtube.commentThreads().list(
        part = "snippet",
        videoId = videoid,
        maxResults = 100
    )

    response = request.execute()
    
    for i in range(100):
        comments.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textDisplay"])

    return comments

