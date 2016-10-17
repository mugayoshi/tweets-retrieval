import sys
import io
import time

from tweepy.streaming import StreamListener

from streaming.tweet import Tweet

class Listener(StreamListener):
    def __init__(self, api, output_file, max_count=0):
        super(Listener, self).__init__(api)
        self.count = 0    # How many tweets have been streamed
        self.max_count = max_count # max tweets to stream. 0 for infinite
        self.output_file = output_file
        self.debug_file = io.open("data/debug_with_api.txt","w")
    def on_data(self, data):
        print(data,file=self.debug_file)
        tweet = Tweet(data)
        t = tweet.preprocess()
        if t and tweet.isTagged():
            print(",".join(tweet.hashtags)+"\t"+t,file=self.output_file)
            self.count += 1
            if self.count == self.max_count: exit()

        # try:
        #     tweet = Tweet(data)
        #     t = tweet.preprocess()
        #     if t and tweet.isTagged():
        #         print(",".join(tweet.hashtags)+"\t"+t,file=self.output_file)
        #         self.count += 1
        #         if self.count == self.max_count: exit()
        # except Exception as e:
        #     print("Twitter restriction handled")
        #     print("Waiting...")
        #     time.sleep(30)
        #     print("Ok, now streaming again")
        #     pass
        return True

    def on_error(self, status):
        if status_code == 429:
            return False
        print("Error !!!", status)
