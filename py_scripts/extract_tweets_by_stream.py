import io, json
import twitter
import sys
import time
from urllib2 import URLError
from httplib import BadStatusLine

from credentials import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET
import common_functions as cf
from datetime import datetime
from datetime import timedelta

def oauth_login():
	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)

	twitter_api = twitter.Twitter(auth=auth)
	return twitter_api

def save_json(filename, data):
	with io.open(jsonfilepath.format(filename), 'w', encoding='utf-8') as f:
		f.write(unicode(json.dumps(data,ensure_ascii=False)))
		
	return

def validateTweet(tweet, emotion):
	words = tweet.split(' ')
	opposite_emotion = []
	if emotion == 'pos':
		opposite_emotion = getEmoticonList('neg')
	elif emotion == 'neg':
		opposite_emotion = getEmoticonList('pos')
	else:
		print 'argument ' + emotion + ' is wrong'
		return False
	for word in words:
		if 'RT' in word:
			return False
		elif '@' in word:
			return False
		elif 'http' in word or 'http' in word:
			return False
		
		if word in opposite_emotion:
			print 'there is an emoticon of the oposite emotion in this tweet'
			print '-->' + tweet
			print '--------------------------------'
			return False
	return True

def getEmoticonList(emotion):
	smiley = [':-)', ':-]', ':-3', ':->', '8-)', ':-}', ':o)', ':c)', ':^)', ':)', ':]', ':>', '8)', ':}', '=]', '=)', ':-))']
	laugh = [':-D', '8-D', 'x-D', 'X-D', 'B^D', ':D', '8D', 'xD', 'XD', '=D', '=3', ":'-)", ":')"]
	others = [':-*', ':*', ':x', '<3', '\o/']
	positive_emoticons = smiley + laugh + others
	#positive_emoticons = [':-)', ':-]', ':-3'. ':->', '8-)', ':-}', ':o)', ':c)', ':^)', ':)', ':]', ':>', '8)', ':}', '=]', '=)', ':-))', ':-D', '8-D', 'x-D', 'X-D', 'B^D', ':D', '8D', 'xD', 'XD', '=D', '=3', ":'-)", ":')", ':-*', ':*', ':x', '<3', '\o/']
	sad_angry = [':-(', ':(', ':c', ':-c',  ':<', ':-<', ':-[', ':[', ':-||', '>:[', ':{', ':@', '>:(']
	skeptical_annoyed = [':-/', ':/', ':-.', '>:\\', '>:/', ':\\', '=/', '=\\', ':L', ':=L', ':S']
	crying = [":'-(", ":'(", "('_')", '(/_;)', '(T_T)', '(;_;)', '(;_;', '(;_:)', '(;O;)']
	indecision = [':-|', ':|']
	negative_emoticons = sad_angry + skeptical_annoyed + crying + indecision
	#negative_emoticons = [':-(', ':(', ':c', ':-c', ':<', ':-<', ':-[', ':[', ':-||', '>:[', ':{', ':@', '>:(', ':-/', ':/', ':-.', '>:\\', '>:/', ':\\', '=/', '=\\', ':L', ':=L', ':S', ':-|',':|']

	if emotion == 'pos':
		return positive_emoticons
	elif emotion == 'neg':
		return negative_emoticons
	
	return ''

def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):
	def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
		if wait_period > 3600:
			print >> sys.stderr, 'too many retries, quitting'
			raise e

		if e.e.code == 401:
			print >> sys.stderr, 'encountered 401 error(Not Authorised)'
			return None
		elif e.e.code == 404:
			print >> sys.stderr, 'encountered 404 error(Not Found)'
			return None
		elif e.e.code == 429:
			print >> sys.stderr, 'encountered 429 error(Rate Limit Exceeded)'
			if sleep_when_rate_limited:
				print >> sys.stderr, 'Retrying in 15 minutes...zz....'
				sys.stderr.flush()
				time.sleep(60*15 + 5)
				print >> sys.stderr, '.zzz.. Awake now and trying again.'
				return 2
			else:
				raise e
		elif e.e.code in (500, 502, 503, 504):
			print >> sys.stderr, 'encountered %i error. retrying in %i seconds' % (e.e.code, wait_period)
			time.sleep(wait_period)
			wait_period *= 1.5
			return wait_period
		else:
			raise e
		# end of handle_twitter_http_error

	wait_period = 2
	error_count = 0

	while True:
		try:
			return twitter_api_func(*args, **kw)
		except twitter.api.TwitterHTTPError, e:
			error_count = 0
			wait_period = handle_twitter_http_error(e, wait_period)
			if wait_period is None:
				return
		except URLError, e:
			error_count += 1
			print >> sys.stderr, "URLError encountered continuing. "
			if error_count > max_errors:
				print >> sys.stderr, "too many consecutive errors...bailing out."
				raise
		except BadStatusLine, e:
			error_count += 1
			print >> sys.stderr, "BadStatusError encountered. continuing. "
			if error_count > max_errors:
				print >> sys.stderr, "Too many consecutive errors... bailing out. "
				raise
	
def obtainTweetsFromStream(twitter_api, q, lang, emotion, max_results):
	kw = {}
	kw['track'] = q
	kw['language'] = lang
	twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
	tweets = make_twitter_request(twitter_stream.statuses.filter, **kw)
	#max_results = 200#can be modified
	
	date = time.strftime("%d%b%Y%H%M")
	file_name = date + "_" + lang + "_" + emotion + "_from_stream.txt"#this text file should be moved to another directory
	out_file_path = "/home/muga/twitter/tweets_from_stream/training/"
	cf.validate_directory(out_file_path, True)
	output = open(out_file_path + file_name, 'w')
	
	start_time = datetime.now()
	count = 0
	for tweet in tweets:
		if 'text' in tweet:
			txt = tweet['text']
		else:
			break#goes outside of this for loop
		if validateTweet(txt, emotion):
			s = json.dumps(tweet['text'], indent=1)
			#print s + ', ' + tweet['created_at'].encode('utf-8')
			output.write(s + ', ' + tweet['created_at'].encode('utf-8') + '\n')
			count += 1
			if count % 100 == 0:
				print  txt + ' : ' + str(count) + ' out of ' + str(max_results)
		if count > max_results:
			cf.write_exec_time(start_time, output)
			return

	print 'goes into the while loop'
	#while len(tweets) > 0 and count < max_results:
	while count < max_results:
		tweets = make_twitter_request(twitter_stream.statuses.filter, **kw)
		for tweet in tweets:
			if 'text' in tweet:
				txt = tweet['text']
			else:
				break #goes outside of this for loop
			if validateTweet(txt, emotion):
				s = json.dumps(tweet['text'], indent=1)
				output.write(s + ', ' + tweet['created_at'].encode('utf-8') + '\n')
				count += 1
				if count % 100 == 0:
					print  txt + ' : ' + str(count) + ' out of ' + str(max_results)
	print 'goes out from the while loop'
	output.close()
	print 'Extracting ' + emotion + ' tweets of ' + lang + ' has done.'

	cf.write_exec_time(start_time, output)
	return
	

def main():

	argvs = sys.argv
	if len(argvs) <= 3:
		print 'please input language, emotion and number of retrieved tweets. if necessary, also user name'
		quit()
	lang = argvs[1]
	#q = ':), :D, :-), ;)'
	languages = ['en', 'fr', 'es', 'de', 'pt']
	if not lang in languages:
		print 'this language is not valid'
		quit()
	emotion = argvs[2]
	if emotion == 'pos':
		q = ':), :-), ^), :], 8), =), :-D, XD, :D, 8D, =D, ;-), ;), ;D, \o/'
	elif emotion == 'neg':
		q = ":-(, :(, :c, :-/, :/, :S, :'(, :|"
	else:
		print 'emotion ' + emotion + ' is incorrect'
		quit()
	max_results = int(argvs[3])
	if len(argvs) == 5:
		twitter_api = cf.authentication_twitter(argvs[4])
	else:
		twitter_api = oauth_login()
	obtainTweetsFromStream(twitter_api, q, lang, emotion, max_results)
	
if __name__ == "__main__":
	main()
