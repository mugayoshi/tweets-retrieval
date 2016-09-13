import twitter
import json
CONSUMER_KEY='yh0ltpdidxnb4y10h1zUOmz20'
CONSUMER_KEY_SECRET='XjJiiuHV7SWdYEUOuzTcFhLef0bmawoAJSisKM52pApd6gfWho'
OAUTH_TOKEN='574115777-FpPvFcducoKtQLrNGrnIUh7BgKKcciUoa8En9L5Q'
OAUTH_TOKEN_SECRET='8owLiHDqv8YplH5zriQ4MO0x5QocPT4ywpDtFNK34OV6W'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)

twitter_api = twitter.Twitter(auth=auth)

q = ""
#latitude = 48.861141
print "latitude = ",
latitude = input()
#35.670479
print "longitude = ",
longitude = input()
#longitude = 2.335620
#139.740921
max_range = 1
num_results = 500
#outfile = ""

last_id = None

count = 100

search_results = twitter_api.search.tweets(q=q, geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count=count, max_id=last_id, lang="en")

statuses = search_results['statuses']

for _ in range(100):
    print "length of statuses", len(statuses)
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e:
        break

    kwargs = dict([ kv.split('=') for kv in next_results[1:].split('&') ])
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']

if len(statuses) > 0:
    for status in statuses:
        print json.dumps(status['text'], indent=1)
#    print json.dumps(statuses[0], indent=1)
else:
    print "no result"
