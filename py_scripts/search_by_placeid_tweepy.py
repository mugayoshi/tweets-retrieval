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
	for result in Cursor(api.search, q=query, lang=lang, retry_count=5, retry_delay=5).items(max_count):
		s = result.text
		if validateTweet(s) == False:
			continue
		created_time = datetime.strftime(result.created_at, '%H:%M:%S on %d/%b/%Y')
		output.write(s.encode('utf-8') + ', ' + created_time.encode('utf-8') + '\n')
		retrieved_tweets += 1

	return retrieved_tweets

def getPlaceID(city_name):
	data_path = '/home/muga/twitter/place_id_data/'
	file_name = ''
	#print 'city name: ' + city_name
	for f in os.listdir(data_path):
		if city_name in f and f.endswith('txt') and 'city' in f:#for now specifies only 'city'
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
	if len(argvs) == 4:
		city_name = argvs[1]
		lang = argvs[2]
		file_name = "tweets_" + date + "_" + lang + "_"+ city_name + ".txt"
		num_results = int(argvs[3])#argumets from command line are initially string type !!!!
	else:
		print 'please input city name, languange and number of retrieved tweets'
		quit()
		#file_name = "tweets-" + date + "-" + city_name + ".txt"
	file_name = file_name.replace(' ', '')
	out_file_path = '/home/muga/twitter/tweets_from_searchAPI/tweepy/'
	output = open(out_file_path + file_name, 'w')

	start_time = datetime.now()

	place_id_dict = getPlaceID(city_name)
	retrieved_tweets = 0
	query = ''
	while retrieved_tweets < num_results:
		for place in place_id_dict.keys():
			place_name = place_id_dict[place]
			q = "place:%s" % place 
			query = get_query(q)
			current_time = datetime.now()
			place_info = "\n------- " + place_name[0] + "at " + datetime.strftime(current_time, '%H:%M:%S on %d/%b/%Y') + " -------\n"
			output.write(place_info)

			retrieved_tweets += search(query, lang, output)#!!!! search function returns the number of the retrieved tweets
		#the end of the for loop for each place
		print str(retrieved_tweets) + ' have been retrieved until now. out of ' + str(num_results)
	#the end of the while loop

	print 'goes out of the while loop'
	print str(retrieved_tweets) + ' are retrieved'
	end_time = datetime.now()
	exec_time = 'Execution time:%s' % (end_time - start_time)
	print exec_time
	output.write('\n\n\n' + exec_time + '\n')
	output.close()
if __name__ == '__main__':
	main()
