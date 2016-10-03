import sys

from Tweet import Tweet
from tweepy.streaming import StreamListener

class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet = Tweet(data)
        t = tweet.preprocess()
        if t and tweet.isTagged():
            print(",".join(tweet.hashtags)+"\t"+t,file=sys.stdout)
        return True

    def on_error(self, status):
        print("Error:", status)
