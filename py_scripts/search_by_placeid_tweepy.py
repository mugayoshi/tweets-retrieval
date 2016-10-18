import sys
import io
from datetime import datetime

from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor

from credentials import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET
import time
import os
#def search(query, lang, geocode="", max_count=100):
def search(query, lang, output, max_count=100):
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
	auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	#print("QUERY:[",query,"]", "OUTPUT:", output_file.name, file=output_file)
	retrieved_tweets = 0
	for result in Cursor(api.search, q=query, lang=lang).items(max_count):
		s = result.text + "\n"
		if validateTweet(s) == False:
			continue
		output.write(s.encode('utf-8'))
		retrieved_tweets += 1

	return retrieved_tweets

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


def validateTweet(tweet):
	words = tweet.split(' ')
	for word in words:
		if '@' in word:
			return False
		elif 'http' in word or 'http' in word:
			return False
		
	return True


def get_query(q, retweets=False, since="", until="", geocode="",):
	#q = " OR ".join(keywords)
	q += ("" if retweets else " -filter:retweets")
	q += (" since:" + since if since else "")
	q += (" until:" + until if until else "")
	return q

def main():
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
	out_file_path = '/home/muga/twitter/tweets_from_searchAPI/'
	output = open(out_file_path + file_name, 'w')

	num_results = 100
	start_time = datetime.now()

	place_id_dict = getPlaceID(city_name)
	retrieved_tweets = 0
	query = ''
	while retrieved_tweets < num_results:
		for place in place_id_dict.keys():
			place_name = place_id_dict[place]
			q = "place:%s" % place 
			query = get_query(q)
			place_info = "------- " + place_name[0] + " -------\n"
			output.write(place_info)

			retrieved_tweets += search(query, lang, output)#!!!! search function returns the number of the retrieved tweets
		#the end of the for loop for each place
		print str(retrieved_tweets) + ' have been retrieved until now.'
	#the end of the while loop

	print 'goes out of the while loop'
	output.close()
	print str(retrieved_tweets) + ' are retrieved'
	end_time = datetime.now()
	print 'Execution time:%s' % (end_time - start_time)
if __name__ == '__main__':
	main()
