import googleapiclient.discovery
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
