import sys
import time
from urllib2 import URLError
from httplib import BadStatusLine
import json
import twitter

def oauth_login():
	CONSUMER_KEY='yh0ltpdidxnb4y10h1zUOmz20'
	CONSUMER_KEY_SECRET='XjJiiuHV7SWdYEUOuzTcFhLef0bmawoAJSisKM52pApd6gfWho'
	OAUTH_TOKEN='574115777-FpPvFcducoKtQLrNGrnIUh7BgKKcciUoa8En9L5Q'
	OAUTH_TOKEN_SECRET='8owLiHDqv8YplH5zriQ4MO0x5QocPT4ywpDtFNK34OV6W'

	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)

	twitter_api = twitter.Twitter(auth=auth)
	return twitter_api

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


def harvest_user_timeline(twitter_api, screen_name = None, user_id = None, max_results = 10000):
	assert (screen_name != None) != (user_id != None), "Must have screen_name or user_id, but not both"

	kw = {'count': 200, 'trim_user': 'true', 'include_rts': 'true', 'since_id': 1}
	if screen_name:
		kw['screen_name'] = screen_name
	else:
		kw['user_id'] = user_id

	
	max_pages = 16
	results = []

	tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
	
	if tweets is None:
		tweets = []
	
	results += tweets

	print >> sys.stderr, 'Fetched %i tweets' % len(tweets)

	page_num = 1

	if max_results == kw['count']:
		page_num = max_pages
	
	while page_num < max_pages and len(tweets) > 0 and len(results) < max_results:
		kw['max_id'] = min([ tweet['id'] for tweet in tweets]) - 1
		tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
		results += tweets

		print >> sys.stderr, 'Fetched %i tweets ' % (len(tweets),)

		page_num += 1
	
	print >> sys.stderr, 'Done fetching tweets'

	return results[:max_results]

def validateTweet(tweet):
	words = tweet.split(' ')
	
	for word in words:
		if 'RT' in word:
			return False
		elif '@' in word:
			return False
	
	return True



def main():
	argvs = sys.argv
	if len(argvs) < 3:
		print 'account name is required for this script.'
		quit()
	account_name = argvs[1]
#screen_name is basically userid (?)
	date = time.strftime("%d%b%Y%H%M")
	lang = argvs[2]
	languages = ['en', 'fr', 'es', 'de', 'pt']
	if not lang in languages:
		print 'this language is not valid'
		quit()
	
	out_file_path = "/home/nak/muga/twitter/tweets_from_stream"
	file_name = "tweets_" + date + "_" + lang + "_neu_"+ account_name + ".txt"#this text file should be moved to another directory
	output = open(out_file_path + file_name, 'w')

	num_retrieved_tweets = 1500
	twitter_api = oauth_login()
	tweets = harvest_user_timeline(twitter_api, screen_name=account_name, max_results=num_retrieved_tweets)
	count = 0
	while count < num_retrieved_tweets:
		for tweet in tweets:
			if not validateTweet(tweet['text']):
				continue
			s = json.dumps(tweet['text'], indent=1) + "\n"#need to modify !!
			output.write(s)
			count = count + 1
		#the end of the for loop

		print 'count: ' + str(count) + '. it is going to another query.'
		tweets = harvest_user_timeline(twitter_api, screen_name=account_name, max_results=num_retrieved_tweets)
	output.close()
	print 'Done. number of retrieved tweets of ' + account_name + ' are ' + str(count)
if __name__ == "__main__":
	main()
