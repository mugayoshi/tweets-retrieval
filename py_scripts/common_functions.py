import os
import csv
from datetime import datetime
import time
from tweepy import API
from tweepy import OAuthHandler
from settings_adam import OAUTH_TOKEN_adam, OAUTH_TOKEN_SECRET_adam, CONSUMER_KEY_adam, CONSUMER_KEY_SECRET_adam
import twitter
from credentials import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET
def validate_directory(path, create_dir=False):
	if not os.path.exists(path):
		print path + ' is not found.'
		if create_dir:
			os.makedirs(path)
			print 'directory ' + path + ' is created'
			time.sleep(5)#sleeps for 5 secs
		else:
			print 'abort'
			quit()
	return

def validate_language(lang):
	languages = ['en', 'fr', 'es', 'de', 'pt']
	if not lang in languages:
		print 'this language is not valid'
		quit()

	return True

def extract_tweet_from_test_data(filename):
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	data = []
	header = next(csv_reader)
	for row in csv_reader:
		try:
			row[0].decode('utf-8', 'strict') #depends on file
		except:
			continue
		data.append(row[0]) #depends on file

	if len(data) == 0:
		print 'no data'
		quit()
	else:
		print 'this file contains ' + str(len(data)) + ' tweets'
			
	return data

def write_exec_time(start_time, output):
	end_time = datetime.now()
	exec_time = 'Execution time:%s' % (end_time - start_time)
	print exec_time
	output.write('\n\n\n' + exec_time + '\n')
	return

def get_emotion_label(label):
	if label == 0:
		return 'pos'
	elif label == 1:
		return 'neg'
	elif label == 2:
		return 'neu'
	else:
		print 'something is wrong with this ' + str(label)
		quit()

def authentication_tweepy(user='muga'):
	if user == 'muga':
		auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
		auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	elif user == 'adam':
		auth = OAuthHandler(CONSUMER_KEY_adam, CONSUMER_KEY_SECRET_adam)
		auth.set_access_token(OAUTH_TOKEN_adam, OAUTH_TOKEN_SECRET_adam)
	else:
		print 'user ' + user + ' is wrong'
		quit()

	api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	return api

def authentication_twitter(user='muga'):
	if user == 'muga':
		auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)
		twitter_api = twitter.Twitter(auth=auth)

	elif user == 'adam':
		auth = twitter.oauth.OAuth(OAUTH_TOKEN_adam, OAUTH_TOKEN_SECRET_adam, CONSUMER_KEY_adam, CONSUMER_KEY_SECRET_adam)
	else:
		print 'user ' + user + ' is wrong'
		quit()
	
	twitter_api = twitter.Twitter(auth=auth)
	return twitter_api

