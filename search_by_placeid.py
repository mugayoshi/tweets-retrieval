import sys
import os
import twitter
import json

def getPlaceID(city_name):

	file_name = "place-id-" + city_name + ".txt"
	if os.path.isfile(file_name) == False:
		return ''

	input = open(file_name, 'r')
	s = input.readline()

	place_id_dict = {}

	while s: #until the end of the file
		splitted_line =  s.split(':')
		place_id = splitted_line[0]
		place_fullname = splitted_line[1]
		place_name = splitted_line[2]
		place_list = [place_fullname, place_name]
		place_id_dict[place_id] = place_list
#print s
		s = input.readline()
	return place_id_dict

def searchTweetByPlaceID(api, place_id):
	last_id = None
	count = 1000
	#get language parameter
	lang = ''
	argvs = sys.argv
	if len(argvs) > 1:
		lang = argvs[1]

	search_results = api.search.tweets(q="place:%s" % place_id ,count=count, max_id=last_id, lang=lang)

	results = search_results['statuses']

	for _ in range(100):
		print "length of results", len(results)
		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e:
			break

		kwargs = dict([ kv.split('=') for kv in next_results[1:].split('&') ])
		search_results = api.search.tweets(**kwargs)
		results += search_results['statuses']


	return results

def main():
	CONSUMER_KEY='yh0ltpdidxnb4y10h1zUOmz20'
	CONSUMER_KEY_SECRET='XjJiiuHV7SWdYEUOuzTcFhLef0bmawoAJSisKM52pApd6gfWho'
	OAUTH_TOKEN='574115777-FpPvFcducoKtQLrNGrnIUh7BgKKcciUoa8En9L5Q'
	OAUTH_TOKEN_SECRET='8owLiHDqv8YplH5zriQ4MO0x5QocPT4ywpDtFNK34OV6W'

	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)

	twitter_api = twitter.Twitter(auth=auth)
#    num_results = 500
	print "place name: ", 
	city_name = raw_input()

#get place id
	place_id_dict = getPlaceID(city_name)
	for place in place_id_dict.keys():
		results = searchTweetByPlaceID(twitter_api, place)

		if len(results) > 0:
			for result in results:
				print json.dumps(result['text'], indent=1)
#print json.dumps(results[0], indent=1)
		else:
			print "no result from " + place[0] + place[1] 

if __name__ == "__main__":
	main()
