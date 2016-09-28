from tweepy.streaming import StreamListener

class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print "Error:", status
