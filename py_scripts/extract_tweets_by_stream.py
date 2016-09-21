import io, json
import twitter
import sys
import time
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
			print tweet
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
	
	#lang = 'en'
	twitter_api = oauth_login()
	twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
	stream = twitter_stream.statuses.filter(track=q, language=lang)
	
	date = time.strftime("%d-%b-%Y:%H:%M")
	file_name = "tweets-" + date + "-" + lang + "-" + emotion + "-from_stream.txt"#this text file should be moved to another directory
	output = open(file_name, 'w')

	count = 0
	number_of_tweet = 5000
	for tweet in stream:
		txt = tweet['text']
		if validateTweet(txt, emotion):
			s = json.dumps(tweet['text'], indent=1) + "\n"
			output.write(s)
			count = count + 1
			if count % 100 == 0:
				print txt
		if count > number_of_tweet:
			break
	output.close()
	print 'Extracting ' + emotion + ' tweets of ' + lang + ' has done.'
if __name__ == "__main__":
	main()
