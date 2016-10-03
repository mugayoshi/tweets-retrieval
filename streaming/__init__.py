# Streaming module
# Streams preprocessed tweets in the following format
# hashtag1,hashtag2,...[tab]tweet's content

import sys

from tweepy import OAuthHandler
from tweepy import Stream

from streaming.tweet import Tweet
from streaming.listener import Listener
from streaming.credentials import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

def stream(keywords=[],language='',output_file="",max_count=0):
    # Init Tweet stream
    listener = Listener(output_file,max_count)
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    
    # Stream search results into the console
    stream.filter(languages=[language],track=keywords)

    
