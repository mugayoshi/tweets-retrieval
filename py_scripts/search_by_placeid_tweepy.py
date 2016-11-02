import sys
import io
from datetime import datetime
from datetime import timedelta

from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor

from credentials import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET
import time
import os
import common_functions as cf

def search(query, lang, output, max_count=10000):#mac count is set to 10000 in Adam's version
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
	auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	retrieved_tweets = 0
	six_days_ago = (datetime.now() - timedelta(days=6)).date()#due to the time difference, it is set to be 6 days ago.
	since_date = six_days_ago.strftime('%Y-%m-%d')
	yesterday = (datetime.now() - timedelta(days=1)).date()#due to the time difference, it is set to be 6 days ago.
	until_date = yesterday.strftime('%Y-%m-%d')

	for result in Cursor(api.search, q=query, lang=lang, since=since_date, until=until_date).items(max_count):
		s = result.text
		if validateTweet(s) == False:
			continue
		created_time = datetime.strftime(result.created_at, '%H:%M:%S on %d/%b/%Y')
		output.write(s.encode('utf-8') + ', ' + created_time.encode('utf-8') + '\n')
		retrieved_tweets += 1

	return retrieved_tweets

def getPlaceID(city_name):
	data_path = '/home/muga/twitter/place_id_data/' + city_name + '/'
	file_name = ''
	for f in os.listdir(data_path):
		if not 'uniq' in f:#the name of the input file has to contain 'uniq' 
			continue
		if city_name in f and f.endswith('txt') and f.startswith('placeid'):
			file_name = data_path + f
			#print 'file_name: ' + file_name
			break

	if len(file_name) == 0:
		print 'The Input File is not Found. Abort'
		quit()

	input = open(file_name, 'r')
	s = input.readline()

	place_id_dict = {}
	while s: #until the end of the file
		if s.startswith('city name') or s.startswith('place name'):
			s = input.readline()
			continue
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
	out_file_path = '/home/muga/twitter/tweets_from_searchAPI/tweepy/' + city_name + '/'
	cf.validate_directory(out_file_path)

	output = open(out_file_path + file_name, 'w')

	start_time = datetime.now()

	place_id_dict = getPlaceID(city_name)
	retrieved_tweets = 0
	query = ''
	for place in place_id_dict.keys():
		place_name = place_id_dict[place]
		q = "place:%s" % place 
		query = get_query(q)
		current_time = datetime.now()
		place_info = "\n------- " + place_name[0] + " at " + datetime.strftime(current_time, '%H:%M:%S on %d/%b/%Y') + " -------\n"
		output.write(place_info)

		obtained_tweets = search(query, lang, output)#!!!! search function returns the number of the retrieved tweets
		print str(obtained_tweets) + ' are retrieved in this loop from ' + place_name[0]
		retrieved_tweets += obtained_tweets
#the end of the for loop for each place

	print str(retrieved_tweets) + ' are retrieved'
	end_time = datetime.now()
	exec_time = 'Execution time:%s' % (end_time - start_time)
	print exec_time
	output.write('\n\n\n' + exec_time + '\n')
	output.close()
if __name__ == '__main__':
	main()
