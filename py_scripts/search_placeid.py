import twitter
import json
CONSUMER_KEY='yh0ltpdidxnb4y10h1zUOmz20'
CONSUMER_KEY_SECRET='XjJiiuHV7SWdYEUOuzTcFhLef0bmawoAJSisKM52pApd6gfWho'
OAUTH_TOKEN='574115777-FpPvFcducoKtQLrNGrnIUh7BgKKcciUoa8En9L5Q'
OAUTH_TOKEN_SECRET='8owLiHDqv8YplH5zriQ4MO0x5QocPT4ywpDtFNK34OV6W'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)

twitter_api = twitter.Twitter(auth=auth)
print "parameter for geo search"
print "query = ",
query = raw_input()
print "granularity = ",
granularity = raw_input()

result = twitter_api.geo.search(query=query, granularity=granularity)

places = result['result']['places']
place_id_dict = {}
for place in places:
    place_full_name = place['full_name']
    place_name = place['name']
    place_id = place['id']
    place_list = [place_full_name, place_name]
    place_id_dict[place_id] = place_list
file_name = "place-id-" + query + ".txt"
output = open(file_name, 'w')

for p_id in place_id_dict:
    #print p + " ----> id:  " + place_dict[p] + "\n"
    s = p_id + ": " + place_id_dict[p_id][0] + ": " + place_id_dict[p_id][1]+ "\n"
    #decode s as UTF-8 string
    output.write(s.encode('utf-8'))
output.close()
