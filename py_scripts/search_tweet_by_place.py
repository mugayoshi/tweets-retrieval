import twitter
import json
CONSUMER_KEY='yh0ltpdidxnb4y10h1zUOmz20'
CONSUMER_KEY_SECRET='XjJiiuHV7SWdYEUOuzTcFhLef0bmawoAJSisKM52pApd6gfWho'
OAUTH_TOKEN='574115777-FpPvFcducoKtQLrNGrnIUh7BgKKcciUoa8En9L5Q'
OAUTH_TOKEN_SECRET='8owLiHDqv8YplH5zriQ4MO0x5QocPT4ywpDtFNK34OV6W'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)

twitter_api = twitter.Twitter(auth=auth)

#q = "*&geocode=48.861141,2.335620,1000km"
q = "&lang=pt"
maxcount = 1000
maxid = 0
count = 100
search_results = twitter_api.search.tweets(q=q, count=count)

statuses = search_results['statuses']
i = 0
while True:
    for status in statuses:
        if maxid >= status.id:
            maxid = status.id
         
        print "length of statuses", len(statuses)
        i = i + 1
    if len(stasues) == 0:
        break
    if maxcount <= i:
        break
    print maxid
    
    print "length of statuses", len(statuses)
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e:
        break

    kwargs = dict([ kv.split('=') for kv in next_results[1:].split('&') ])
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']

for status in statuses:
    print json.dumps(status, indent=1)
