import sys
import io
from datetime import datetime

from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor

from tweet import Tweet
from credentials import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

def search(query,output_file,
           lang="en",
           geocode="",
           max_count=100000):
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth,
              wait_on_rate_limit=True,
              wait_on_rate_limit_notify=True)

    print("QUERY:[",query,"]", "OUTPUT:", output_file.name, file=output_file)
    count = 0
    ok_count = 0
    for result in Cursor(api.search,
                         q=query,
                         lang=lang).items(max_count):
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
    q = " OR ".join(keywords)
    q += ("" if retweets else " -filter:retweets")
    q += (" since:" + since if since else "")
    q += (" until:" + until if until else "")
    return q

if __name__ == '__main__':
    # keywords = sys.argv[1:]
    # output_path = "data/" + "_".join(keywords) + ".txt"
    # with io.open(output_path, 'w') as output_file:
    #    streaming.stream(keywords,language='en',output_file=output_file,max_count=10000)
    
    # q = input("Search for:")
    keywords = []
    q = get_query(keywords)
    output_path = "/home/local/data/stream_output.txt"
    start_time = datetime.now()
    with io.open(output_path, 'w') as f:
        search(q,f)
    end_time = datetime.now()
    print("Execution time:", end_time - start_time)


