# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
from dotenv import load_dotenv
import pandas as pd
import re
import urllib.parse as up

from googleapiclient.discovery import build

from utils import comments
from utils.comments import process_comments, make_csv
from Mongo import *


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

def parseURL(URL):
    try:
        URL = up.urlparse(URL)
        query = up.parse_qs(URL.query)
        videoId = query["v"][0]
        return videoId
    except:
        print("Please Enter a Valid URL")
        return None
        
def main():
    videoLink = input('Enter Video Link ')
    videoId = parseURL(videoLink)
    if(videoId == None):
        return 
    
    if(existMongo('Youtube' , videoId)):
        print('Last Comment On:' , lastUpdate('Youtube', videoId))

        yesno = input("Do you want to update? Y/N \n")
        if(yesno == 'Y' or yesno == 'y'):
            print('Querying API ',  sep = '')
            df = pd.DataFrame(comment_threads(videoId, to_csv = False))
            df['Sentiment'] = ''
            df = df[['commentId','publishedAt', 'likeCount','Sentiment', 'textOriginal']]
            print("Finish Formatting and Updating")
            importCol(df , videoId)
    
    else:
        print('Querying API ',  sep = '')
        df = pd.DataFrame(comment_threads(videoId, to_csv = False))
        df['Sentiment'] = ''
        df = df[['commentId','publishedAt', 'likeCount','Sentiment', 'textOriginal']]
        print("Finish Formatting and Updating")
        importCol(df , videoId)
        #aa

    

    
if __name__ == "__main__":
    main()
    
    
