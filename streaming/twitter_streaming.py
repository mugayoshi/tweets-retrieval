import sys

from tweepy import OAuthHandler
from tweepy import Stream

from Listener import StdOutListener
from settings import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

if __name__ == '__main__':
    # Tweets Search keywords
    keywords = []
    if sys.argv[1:]:
        keywords = sys.argv[1:]
        # [unicode(w, encoding='utf-8') for w in sys.argv[1:]]
    else:
        print("No keywords received in argument. Exiting")
        exit()
    language = 'en'
    # Init Tweet stream
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    
    # Stream search results into the console
    stream.filter(languages=[language],track=keywords)

    
