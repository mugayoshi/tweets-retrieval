import io, json
import twitter
import sys
import time
from urllib2 import URLError
from httplib import BadStatusLine

def oauth_login():
	CONSUMER_KEY='yh0ltpdidxnb4y10h1zUOmz20'
	CONSUMER_KEY_SECRET='XjJiiuHV7SWdYEUOuzTcFhLef0bmawoAJSisKM52pApd6gfWho'
	OAUTH_TOKEN='574115777-FpPvFcducoKtQLrNGrnIUh7BgKKcciUoa8En9L5Q'
	OAUTH_TOKEN_SECRET='8owLiHDqv8YplH5zriQ4MO0x5QocPT4ywpDtFNK34OV6W'

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
	
def obtainTweetsFromStream(twitter_api, q, lang, emotion):
	kw = {}
	kw['track'] = q
	kw['language'] = lang
	twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
	tweets = make_twitter_request(twitter_stream.statuses.filter, **kw)
	max_results = 2000#can be modified
	
	date = time.strftime("%d%b%Y%H%M")
	file_name = "tweets_" + date + "_" + lang + "_" + emotion + "_from_stream.txt"#this text file should be moved to another directory
	out_file_path = "/muga/txt_files/tweets_from_stream/"
	output = open(out_file_path + file_name, 'w')
	
	count = 0
	for tweet in tweets:
		if 'text' in tweet:
			txt = tweet['text']
		else:
			break#goes outside of this for loop
		if validateTweet(txt, emotion):
			s = json.dumps(tweet['text'], indent=1) + "\n"
			output.write(s)
			count = count + 1
			if count % 100 == 0:
				print str(count) + ': ' + txt

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
				s = json.dumps(tweet['text'], indent=1) + "\n"
				output.write(s)
				count = count + 1
				if count % 100 == 0:
					print str(count) + ': ' + txt
	print 'goes out from the while loop'
	output.close()
	print 'Extracting ' + emotion + ' tweets of ' + lang + ' has done.'
	return
	

def main():

	argvs = sys.argv
	lang = argvs[1]
	#q = ':), :D, :-), ;)'
	languages = ['en', 'fr', 'es', 'de', 'pt']
	if not lang in languages:
		print 'this language is not valid'
		quit()
	
	smiley = ':-), :-], :-3. :->, 8-), :-}, :o), :c), :^), :), :], :>,8), :}, =], =), :-))'
	laugh = ":-D, 8-D, x-D, X-D, B^D, :D, 8D, xD, XD, =D, =3, :'-), :')"
	kiss = ':-*, :*, :x'
	wink = ';-), *-), ;-], ;^), :-, ;), *), ;], ;D'
	heart = '<3'
	yay = '\o/'

	sad_angry = ':-(, :(, :c, :-c,  :<, :-<, :-[, :[, :-||, >:[, :{, :@, >:('
	skeptical_annoyed = ':-/, :/, :-., >:\, >:/, :\, =/, =\, :L, :=L, :S'
	crying = ":'-(, :'(, ('_'), (/_;), (T_T), (;_;), (;_;, (;_:), (;O;)"
	troubled = '>.<, (>_<), (>_<)>, (-_-;)'
	looking_down = '(..), (._.)'
	indecision = ':-|, :|'

	emotion = argvs[2]
	if emotion == 'pos':
		q = smiley + ', ' + laugh + ', ' + kiss + ', ' + wink + ', ' + heart + ', ' + yay
	elif emotion == 'neg':
		q = sad_angry + ', ' + skeptical_annoyed + ', ' + crying + ', ' + troubled + ', ' + looking_down + ', ' + indecision
	else:
		print 'emotion ' + emotion + ' is incorrect'
		quit()
	
	twitter_api = oauth_login()
	obtainTweetsFromStream(twitter_api, q, lang, emotion)
	
	
if __name__ == "__main__":
	main()
