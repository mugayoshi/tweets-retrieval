from tweepy import OAuthHandler
from tweepy import Stream

from Listener import StdOutListener
from settings import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)
    # Tweets Search keywords
    keywords = ['presidential']

    # Stream search results into the console
    stream.filter(track=keywords)
