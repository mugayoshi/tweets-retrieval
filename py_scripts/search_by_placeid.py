import sys
import os
import twitter
import json
import time

def getPlaceID(city_name):
	data_path = '/home/muga/twitter/place_id_data/'
	file_name = ''
	print 'city name: ' + city_name
	for f in os.listdir(data_path):
		if city_name in f and f.endswith('txt') and 'city' in f:#for now specifies only 'city'
			file_name = data_path + f
			print 'file_name: ' + file_name
			break
	if len(file_name) == 0:
		print 'The Input File is not Found. Abort'
		quit()

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
		s = input.readline()
	return place_id_dict

def searchTweetByPlaceID(api, place_id, place_name, lang, num_calls):
	last_id = None
	count = 1000
	#get language parameter
	search_results = api.search.tweets(q="place:%s" % place_id ,count=count, max_id=last_id, lang=lang)

	results = search_results['statuses']
	num_calls += 1
	for _ in range(10000):
		print "length of results: " + str(len(results)) + ' from ' + place_name[0] + place_name[1]
		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e:
			break

		kwargs = dict([ kv.split('=') for kv in next_results[1:].split('&') ])
		search_results = api.search.tweets(**kwargs)
		results += search_results['statuses']
		num_calls += 1
		print 'search API has been called ' + str(num_calls) + ' times so far'


	return results, num_calls

def validateTweet(tweet):
	words = tweet.split(' ')
	for word in words:
		if 'RT' in word:
			return False
		elif '@' in word:
			return False
		elif 'http' in word or 'http' in word:
			return False
		
	return True


def main():
	CONSUMER_KEY='yh0ltpdidxnb4y10h1zUOmz20'
	CONSUMER_KEY_SECRET='XjJiiuHV7SWdYEUOuzTcFhLef0bmawoAJSisKM52pApd6gfWho'
	OAUTH_TOKEN='574115777-FpPvFcducoKtQLrNGrnIUh7BgKKcciUoa8En9L5Q'
	OAUTH_TOKEN_SECRET='8owLiHDqv8YplH5zriQ4MO0x5QocPT4ywpDtFNK34OV6W'

	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)
	twitter_api = twitter.Twitter(auth=auth)

	num_results = 1000#!!! this number is variable. !!!

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
	out_file_path = "/home/muga/twitter/tweets_from_searchAPI/"
	output = open(out_file_path + file_name, 'w')

#get place id
	place_id_dict = getPlaceID(city_name)
	retrieved_tweets = 0
	num_calls = 0
	while retrieved_tweets < num_results:
		if num_calls >= 180:
			print 'too many request. sleeps for 15 mins....zzz...'
			time.sleep(60*15 + 5)
			num_calls = 0
		
		for place in place_id_dict.keys():
			if num_calls >= 180:
				print 'too many request. sleeps for 15 mins....zzz...'
				time.sleep(60*15 + 5)
				num_calls = 0

			place_name = place_id_dict[place]
			results, num_calls_updated = searchTweetByPlaceID(twitter_api, place, place_name, lang, num_calls)
			num_calls = num_calls_updated
			place_info = "------- " + place_name[0] + " -------\n"
			output.write(place_info)

			if len(results) == 0:
				print "no result from " + place_name[0] + place_name[1] 
				continue
			for result in results:
				s = json.dumps(result['text'], indent=1) + "\n"#need to modify !!
				if validateTweet(s) == False:
					continue
				output.write(s)
				retrieved_tweets += 1
		#the end of the for loop for each place
		print 'sleeps for half hour to wait for the next loop'
		time.sleep(60 * 30 + 5)
	#the end of the while loop

	print 'goes out of the while loop'
	output.close()
	print str(retrieved_tweets) + ' are retrieved'

if __name__ == "__main__":
	main()
