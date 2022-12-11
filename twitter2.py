import tweepy
import pandas as pd
import os
from dotenv import load_dotenv
from utils import comments
from utils.comments import getUserIdTweetId
# Oauth keys

load_dotenv()
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
bearer_token = os.getenv('bearer_token')


#Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit= True)
client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token,access_token_secret,wait_on_rate_limit=True)

# update these for the tweet you want to process replies to 'name' = the account username and you can find the tweet id within the tweet URL
# name = ''
# tweet_id = ''

# dont touch this one
name = ''
tweet_id = ''
conversation_id = ''
link = ''


link = input('link \n')

name , tweet_id = getUserIdTweetId(link)


replies=[]
responses_from_conversations = []

tweet = client.get_tweet(id = tweet_id ,
                          tweet_fields = 'conversation_id')

conversation_id = tweet.data['conversation_id']
 
for response in tweepy.Paginator(client.search_recent_tweets,
                                query = f'conversation_id:{conversation_id} to:{name}' ,
                                tweet_fields = 'created_at', 
                                user_auth = True).flatten():  
    print(response)
    responses_from_conversations.append(response)


df = pd.DataFrame(responses_from_conversations)
print(df)

df.to_csv('something.csv', encoding= 'utf-8', index = False)
