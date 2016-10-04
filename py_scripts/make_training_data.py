import re
import os
import sys
import time
def replaceURLAndUsername(tweet):
	#tweet_original = tweet.encode('utf-8')
	tweet = tweet.encode('utf-8')
	
	for word in tweet.split(' '):
		if 'http' in word:
			tweet = tweet.replace(word, '~http')
		elif '@' in word:
			tweet = tweet.replace(word, '@user')
		
	return tweet.decode('utf-8')

def writeToFile(lines_of_tweet, output_file, emotion):
	max_tweet = 1000
	if emotion == 'pos':
		sentiment_value = 0
	elif emotion == 'neg':
		sentiment_value = 1
	elif emotion == 'neu':
		sentiment_value = 2
	else:
		print emotion  + ' is invalid'
		quit()
	
	count = 0
	for tweet in lines_of_tweet:
		tweet = replaceURLAndUsername(tweet)
		tweet = re.sub(r'\n+', ' ', tweet)#replace '\n' with a space character
		if emotion == 'pos' or emotion == 'neg':
			tweet = eliminateEmoticons(tweet, emotion)
		if '~http' in tweet and emotion == 'neu':
			tweet = tweet.replace('~http', '')
			tweet = '"' + tweet + '"'
	
		tweet = re.sub(r'[\"]{2,}', '\"', tweet)# this works as same as 'tweet = tweet.replace('\"\"', '\"')'
		
		tweet = re.sub(r'[\-]+', '', tweet)#eliminate hyphens
		tweet = re.sub(r'[ ]{2,}', '', tweet)#eliminate 2 spaces in a tweet
		tweet = re.sub(r'\\ud[a-zA-Z0-9]+', '', tweet) #remove a string such as '\ud***'
		tweet = re.sub(r'(\W+)\1|(..+)\2', '', tweet)#remove consecutive characters e.g.'hiiiii !!!'
		tweet = re.sub(r'&amp;', '&', tweet)
		#tweet = re.sub(r'[ ]$', '', tweet)#remove a space at the end of the sentence
		tweet = re.sub(r'[ ]\"$', '\"', tweet)#remove a space at the end of the sentence
			
		line = '"' + str(sentiment_value) + '", ' + tweet + '\n'
		output_file.write(line.encode('utf-8'))#necessary to encode otherwise cannot write strings
		count += 1
		if count > max_tweet:
			break

	return

def eliminateEmoticons(tweet, emotion):
	#tweet is unicode type
	emoticon_list = getEmoticonList(emotion)
	tweet_str = tweet.encode('utf-8')
	if len(emoticon_list) == 0:
		print 'the list is empty'
		quit()
	for word in tweet_str.split(' '):
		word = word.replace('\"', '') 
		word = word.replace('\n', '') 
		#word_str = word.encode('utf-8')
		if word in emoticon_list:
			tweet = tweet.replace(word, '')
			#print 'replace',
	#print tweet
	return  tweet

def getEmoticonList(emotion):
	smiley = [':-)', ':-]', ':-3', ':->', '8-)', ':-}', ':o)', ':c)', ':^)', ':)', ':]', ':>', '8)', ':}', '=]', '=)', ':-))']
	laugh = [':-D', '8-D', 'x-D', 'X-D', 'B^D', ':D', '8D', 'xD', 'XD', '=D', '=3', ":'-)", ":')"]
	others = [':-*', ':*', ':x', '<3', '\o/']
	positive_emoticons = smiley + laugh + others
	
	sad_angry = [':-(', ':(', ':c', ':-c',  ':<', ':-<', ':-[', ':[', ':-||', '>:[', ':{', ':@', '>:(']
	skeptical_annoyed = [':-/', ':/', ':-.', '>:\\', '>:/', ':\\', '=/', '=\\', ':L', ':=L', ':S']
	crying = [":'-(", ":'(", "('_')", '(/_;)', '(T_T)', '(;_;)', '(;_;', '(;_:)', '(;O;)']
	indecision = [':-|', ':|']
	negative_emoticons = sad_angry + skeptical_annoyed + crying + indecision

	if emotion == 'pos':
		return positive_emoticons
	elif emotion == 'neg':
		return negative_emoticons
	
	return ''



def main():
	if len(sys.argv) < 3:
		print 'the input must have emotion (pos, neg or neu) and output file name)'
		quit()
	target_date = ''
	if len(sys.argv) == 4:
		target_date = sys.argv[3]
	emotion = sys.argv[1]#pos, neg, neu
	file_name = sys.argv[2]
	if not emotion in ['pos', 'neg', 'neu']:
		print emotion + ' is wrong for input'
		quit()

	train_datas_path = '/home/nak/muga/twitter/py_scripts/tweets_from_stream/'
	train_data_files = []
	for f in os.listdir(train_datas_path):
		if not target_date == '' and target_date in f and emotion in f:
			train_data_files.append(f)
		elif target_date == '' and f.endswith('.txt') and emotion in f:
			train_data_files.append(f)
			print 'append ' + f 

	if len(train_data_files) == 0:
		print 'Not Found'
		quit()
	
	out_path = '/home/nak/muga/twitter/data_for_test2/'
	date = time.strftime("%d%b%Y%H%M")
	output_file = open(out_path + date + emotion + '_' + file_name, 'wb')
	
	for f in train_data_files:
		input_file = open('/home/nak/muga/twitter/py_scripts/tweets_from_stream/' + f)
		lines_of_tweet = input_file.readlines()
		#validate each sentence again.
		#in neutral tweets (news accounts) each tweet has URL therefore the URLs should be removed.
		#put affected value pos -> 0, neg -> 1, neu -> 2 ?
		#write
		writeToFile(lines_of_tweet, output_file, emotion)
	output_file.close()
	return


if __name__ == '__main__':
	main()
