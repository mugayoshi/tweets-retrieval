import sys
import os
import twitter
import json
import time

def getPlaceID(city_name):

	file_name = "place-id-" + city_name + ".txt"
	file_path = "/home/nak/muga/twitter/txt_files/" + file_name
	#print file_path
	if os.path.isfile(file_path) == False:
		print file_path
		print "this file doesn't exist"
		quit()

	input = open(file_path, 'r')
	s = input.readline()

	place_id_dict = {}
	while s: #until the end of the file
		splitted_line =  s.split(':')
		place_id = splitted_line[0]
		place_fullname = splitted_line[1]
		place_name = splitted_line[2]
		place_list = [place_fullname, place_name]
		place_id_dict[place_id] = place_list
		s = input.readline()
	return place_id_dict

def searchTweetByPlaceID(api, place_id, place_name):
	last_id = None
	count = 1000
	#get language parameter
	lang = ''
	argvs = sys.argv
	if len(argvs) == 3:
		lang = argvs[2]

	search_results = api.search.tweets(q="place:%s" % place_id ,count=count, max_id=last_id, lang=lang)

	results = search_results['statuses']
	for _ in range(10000):
		print "length of results: " + str(len(results)) + ' from ' + place_name[0] + place_name[1]
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
#open output file
	date = time.strftime("%d%b%Y%H%M")
	argvs = sys.argv
	if len(argvs) == 3:
		city_name = argvs[1]
		lang = argvs[2]
		file_name = "tweets_" + date + "_" + lang + "_"+ city_name + ".txt"
	else:
		print 'please input city name and languange'
		quit()
		#file_name = "tweets-" + date + "-" + city_name + ".txt"
	file_name = file_name.replace(' ', '')
	output = open(file_name, 'w')

#get place id
	place_id_dict = getPlaceID(city_name)
	for place in place_id_dict.keys():
		place_name = place_id_dict[place]
		results = searchTweetByPlaceID(twitter_api, place, place_name)
		place_info = "------- " + place_name[0] + " -------\n"

		#output.write(place_info.decode('utf-8'))
		output.write(place_info)

		if len(results) > 0:
			for result in results:
				#print json.dumps(result['text'], indent=1)
				s = json.dumps(result['text'], indent=1) + "\n"#need to modify !!
				#decode s as UTF-8 string
				#output.write(s.decode('utf-8'))
				output.write(s)
		else:
			print "no result from " + place_name[0] + place_name[1] 

	output.close()

if __name__ == "__main__":
	main()
