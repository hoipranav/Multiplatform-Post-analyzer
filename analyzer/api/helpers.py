import googleapiclient.discovery
import os
import praw


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
        except:
            iter = 0
            return comments_list, "KeyError"

    return comments_list, response["nextPageToken"]

def get_reddit_post_comments(url: str):
    """Uses PRAW to get reddit's posts comments thorugh reddit API"""
    credentials = {"client_id":os.environ["reddit_client"],
               "client_secret":os.environ["reddit_client_secret"],
               "User_agent":"script by u/Pitiful_Confusion156",
               "refresh_token":os.environ["reddit_refresh_token"]}

    reddit = praw.Reddit(client_id=credentials["client_id"],
                        client_secret=credentials["client_secret"],
                        refresh_token=credentials["refresh_token"],
                        user_agent=credentials["User_agent"])
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    with open("reddit_comments.txt", "w") as fl:
        for comment in submission.comments.list():
            fl.write(f"{comment.body}\n")