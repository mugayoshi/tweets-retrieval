import io, json
import twitter
import sys
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

	argvs = sys.argv
	#q = argvs[1]
	q = ':), :D, :-), ;)'
	languages = ['en', 'fr', 'es', 'de', 'pt']
	smiley = ':-), :-], :-3. :->, 8-), :-}, :o), :c), :^), :), :], :>,8), :}, =], =), :-))'
	laugh = ":-D, 8-D, x-D, X-D, B^D, :D, 8D, xD, XD, =D, =3, :'-), :')"
	kiss = ':-*, :*, :x'
	wink = ';-), *-), ;-], ;^), :-, ;), *), ;], ;D'
	heart = '<3'
	yay = '\o/'

	twitter_api = oauth_login()
	twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
	stream = twitter_stream.statuses.filter(track=q, language='de')
	
	#print 'length of stream is ' + len(stream)
	count = 0
	for tweet in stream:
		txt = tweet['text']
		if validateTweet(txt):
			print txt
			count = count + 1
		if count > 100:
			break
	

if __name__ == "__main__":
	main()
