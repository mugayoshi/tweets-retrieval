import os
import csv
from datetime import datetime
import time
from tweepy import API
from tweepy import OAuthHandler
from settings_adam import OAUTH_TOKEN_adam, OAUTH_TOKEN_SECRET_adam, CONSUMER_KEY_adam, CONSUMER_KEY_SECRET_adam
from settings_adam import OAUTH_TOKEN_berta, OAUTH_TOKEN_SECRET_berta, CONSUMER_KEY_berta, CONSUMER_KEY_SECRET_berta
from settings_adam import OAUTH_TOKEN_yuki, OAUTH_TOKEN_SECRET_yuki, CONSUMER_KEY_yuki, CONSUMER_KEY_SECRET_yuki
import twitter
from credentials import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET
def validate_directory(path, create_dir=False):
	if not os.path.exists(path):
		print path + ' is not found.'
		if create_dir:
			os.makedirs(path)
			print 'directory ' + path + ' is created'
			time.sleep(1)#sleeps for 5 secs
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
	elif user == 'berta':
		auth = OAuthHandler(CONSUMER_KEY_berta, CONSUMER_KEY_SECRET_berta)
		auth.set_access_token(OAUTH_TOKEN_berta, OAUTH_TOKEN_SECRET_berta)
	elif user == 'yuki':
		auth = OAuthHandler(CONSUMER_KEY_yuki, CONSUMER_KEY_SECRET_yuki)
		auth.set_access_token(OAUTH_TOKEN_yuki, OAUTH_TOKEN_SECRET_yuki)

	else:
		print 'user ' + user + ' is wrong'
		quit()

	api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	return api

def authentication_twitter(user='muga'):
	if user == 'muga':
		auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)
	elif user == 'adam':
		auth = twitter.oauth.OAuth(OAUTH_TOKEN_adam, OAUTH_TOKEN_SECRET_adam, CONSUMER_KEY_adam, CONSUMER_KEY_SECRET_adam)
	elif user == 'berta':
		auth = twitter.oauth.OAuth(OAUTH_TOKEN_berta, OAUTH_TOKEN_SECRET_berta, CONSUMER_KEY_berta, CONSUMER_KEY_SECRET_berta)
	elif user == 'yuki':
		auth = twitter.oauth.OAuth(OAUTH_TOKEN_yuki, OAUTH_TOKEN_SECRET_yuki, CONSUMER_KEY_yuki, CONSUMER_KEY_SECRET_yuki)

	else:
		print 'user ' + user + ' is wrong'
		quit()
	
	twitter_api = twitter.Twitter(auth=auth)
	return twitter_api

def find_lang(filename):
	languages = ['de', 'en', 'es', 'fr', 'pt']
	for w in filename.split('_'):
		for lang in languages:
			if lang == w:
				return lang
	print filename.split('_')
	print 'return none from find_lang'
	return ''

def getEmoticonList(emotion):
	if emotion == 'pos':
		emoticons = [":)", ":-)", "^)", ":]", "8)", "=)", ":-D", "XD", ":D", "8D", "=D", ";-)", ";)", ";D", "\o/"]
	elif emotion == 'neg':
		emoticons = [":-(", ":(", ":c", ":-/", ":/", ":S", ":'(", ":|"]
	
	return emoticons

def extract_train_data(filename):#for training data
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	non_utf_8 = 0
	header = next(csv_reader)
	pos = 0
	neg = 0
	neu = 0
	n_a = 0
	for row in csv_reader:
		try:
			row[1].decode('utf-8', 'strict') #depends on file
		except:
			#print str(i) + ' ' + row[5] + ' contains non-utf-8 character'
			non_utf_8 = non_utf_8 + 1
			continue
		if row[0] == "2": #neutral
			labels.append(2)
			neu += 1
		elif row[0] == "1": #negative
			labels.append(1)
			neg += 1
		elif row[0] == "0": #positive
			labels.append(0)
			pos += 1
		elif row[0] == "3":
			n_a += 1
			continue
		data.append(row[1]) 
	#end of the for loop
	print 'training data positive: ' + str(pos) + ' negative: ' + str(neg) + ' neutral: ' + str(neu) + ' n/a: ' + str(n_a)
	return (labels, data)

def skip_parameter(score, strategy, lang):
	if lang == 'es':
		if score == 'accuracy':
			return False
		else:
			print 'skip this parameter ' + score 
			return True
	if strategy == 'one_against_one' or strategy == 'one_against_the_rest':
		if score == 'accuracy':
			return False
		else:
			print 'skip this parameter ' + score 
			return True
	else:
		return False
