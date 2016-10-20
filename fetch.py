import sys
import io
from datetime import datetime

from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor

from tweet import Tweet
from credentials import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

def search(query, output_file=sys.stdout, debug_file=None,
           lang="en",
           geocode="",
           max_count=500000):
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
    q = " OR ".join(keywords)
    q += ("" if retweets else " -filter:retweets")
    q += (" since:" + since if since else "")
    q += (" until:" + until if until else "")
    return q

if __name__ == '__main__':
    keywords = ["book", "trump", "flight", "hello", "design", "google", "nexus", "game", "ps4", "xbox", "clinton", "bye", "true", "ddos", "got", "snow", "apple", "iphone", "morning", "makeup", "technology"]
    keywords = ["sarkozy","lepen","hollande","2017"]
    q = get_query(keywords)
    output_path = "/home/local/data/stream_output.txt"
    debug_path = "/home/local/data/debug.txt"
    start_time = datetime.now()
    with io.open(output_path, 'w') as f, io.open(debug_path, 'w') as g:
        search(q,f,g)
    end_time = datetime.now()
    print("Execution time:", end_time - start_time)


