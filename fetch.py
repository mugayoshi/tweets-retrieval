import sys

from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor

from tweet import Tweet
from settings import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

def fetch(query, output_file=sys.stdout, debug_file=None,
           lang="en",
           geocode="",
           max_count=500000):
    '''
    Fetches query results into output_files, and prints raw json results into debug_file
    '''
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth,
              retry_count=10,
              retry_delay=15,
              timeout=60,
              wait_on_rate_limit=True,
              wait_on_rate_limit_notify=True)

    print("QUERY:[",query,"]", "OUTPUT:", output_file.name, file=output_file)
    count = 0
    ok_count = 0
    for result in Cursor(api.search,
                         q=query,
                         lang=lang).items(max_count):
        if debug_file: print(result.text+"\n", file=debug_file)
        tweet = Tweet(result.text)
        t = tweet.preprocess()
        if t and tweet.isTagged():
            print(",".join(tweet.hashtags)+"\t"+t,file=output_file)
            ok_count += 1
        count += 1
        if count % 1000 == 0: print("tweets saved:", ok_count, "/", count)
    print("Loop end:", ok_count, "/", count, "tweets saved")

def get_query(keywords,
          retweets=False,
          since="",
          until="",
          geocode="",):
    '''
    Returns query from list of keywords
    '''
    q = " OR ".join(keywords)
    q += ("" if retweets else " -filter:retweets")
    q += (" since:" + since if since else "")
    q += (" until:" + until if until else "")
    return q
