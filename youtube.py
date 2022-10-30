# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
from dotenv import load_dotenv
import pandas as pd
import re
from Mongo import *

from googleapiclient.discovery import build
from utils import comments

from utils.comments import process_comments, make_csv

load_dotenv()
API_KEY = os.getenv('API_KEY')



youtube = build(
    "youtube", "v3", developerKey = API_KEY)

def comment_threads(ChannelID, to_csv=False):
    
    comments_list = []
    
    request = youtube.commentThreads().list(
        part='snippet',
        order = 'time',
        videoId = ChannelID
    )
    
    response = request.execute()
    comments_list.extend(process_comments(response['items']))    
    
    while response.get('nextPageToken'):
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=ChannelID,
            pageToken=response['nextPageToken']
        )
        comments_list.clear()
        
        response = request.execute()
        comments_list.extend(process_comments(response['items']))
    
    print(f"Finished fetching comments for {ChannelID}. {len(comments_list)} comments found.")
    
    if to_csv:
        make_csv(comments_list, ChannelID)
    
    return comments_list
    
def main():
    videoId = input('Enter video ID ')
    
    print(videoId,'\n','Getting Comments')
    
    #df = comment_threads(videoId, to_csv = True)
    
    df = pd.DataFrame(comment_threads(videoId, to_csv = True))
    
    #df = pd.read_csv(f'comments_{videoId}.csv')
    
    #print(df)
    
    df['Sentiment'] = ''
    df = df[['publishedAt', 'likeCount','Sentiment', 'textOriginal']]
    #print(df)
    
    #df.to_csv(f'{videoId}.csv', index = False)
    
    
    print("Finish Formatting")
    
    #importCol(df , videoId)

if __name__ == "__main__":
    main()
    
    
