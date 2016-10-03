import sys

from tweepy.streaming import StreamListener

from streaming.tweet import Tweet

class Listener(StreamListener):
    def __init__(self, output_file, max_count=0):
        self.count = 0    # How many tweets have been streamed
        self.max_count = max_count # max tweets to stream. 0 for infinite
        self.output_file = output_file
    def on_data(self, data):
        tweet = Tweet(data)
        t = tweet.preprocess()
        if t and tweet.isTagged():
            print(",".join(tweet.hashtags)+"\t"+t,file=self.output_file)
            self.count += 1
            if self.count == self.max_count: exit()
        return True

    def on_error(self, status):
        print("Error:", status)
