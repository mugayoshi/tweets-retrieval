import re
import os
import sys
import time
import common_functions as cf
def extractTweetAndDate(line):
	l = line.split(',')
	if not l or '-------' in l[0] or len(l) == 1:
		return ('','')
	else:
		l[1] = l[1].replace('\n', '')
		return (l[0], l[1])

def replaceURLAndUsername(tweet):
	#tweet = tweet.encode('utf-8')
	
	for word in tweet.split(' '):
		if 'http' in word:
			tweet = tweet.replace(word, '~http')
		elif '@' in word:
			tweet = tweet.replace(word, '@user')
		
	#return tweet.decode('utf-8')
	return tweet

def writeToFile(lines, output_file):
	for line in lines:
		tweet, created_date = extractTweetAndDate(line)
		if not tweet:#if this line does not have a tweet
			continue

		tweet = replaceURLAndUsername(tweet)
		tweet = re.sub(r'\n+', ' ', tweet)#replace '\n' with a space character
		tweet = eliminateEmoticons(tweet)
		tweet = re.sub(r'[\"]{2,}', '\"', tweet)# this works as same as 'tweet = tweet.replace('\"\"', '\"')'
		
		tweet = re.sub(r'[\-]+', '', tweet)#eliminate hyphens
		tweet = re.sub(r'[ ]{2,}', '', tweet)#eliminate 2 spaces in a tweet
		tweet = re.sub(r'\\ud[a-zA-Z0-9]+', '', tweet) #remove a string such as '\ud***'
		tweet = re.sub(r'(\W+)\1|(..+)\2', '', tweet)#remove consecutive characters e.g.'hiiiii !!!'
		tweet = re.sub(r'&amp;', '&', tweet)
		tweet = re.sub(r'[ ]\"$', '\"', tweet)#remove a space at the end of the sentence
		
		line = '"' + tweet + '","' + created_date + '"\n'
		output_file.write(line)
		

	return

def eliminateEmoticons(tweet):
	#tweet is unicode type
	emoticon_list = getEmoticonList('pos')
	emoticon_list += getEmoticonList('neg')
	#tweet_str = tweet.encode('utf-8')
	if len(emoticon_list) == 0:
		print 'the list is empty'
		quit()
	for word in tweet.split(' '):
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
	if len(sys.argv) < 4:
		print 'the input must have city name, language and target date of the text file'
		quit()
	
	city_name = sys.argv[1]
	lang = sys.argv[2]
	target_date = sys.argv[3]
	test_datas_path = '/home/muga/twitter/tweets_from_searchAPI/tweepy/' + city_name + '/'
	cf.validate_directory(test_datas_path)
	test_data_files = []
	for f in os.listdir(test_datas_path):
		if lang in f and target_date in f:
			test_data_files.append(f)
			print f + ' is appended' 
		
	if len(test_data_files) == 0:
		print 'Not Found'
		quit()
	
	confirm = raw_input('it is going to process these files. is it okay ? (yes/no) ' )
	if not confirm.lower() in 'yes':
		print 'abort this program'
		quit()

	out_path = '/home/muga/twitter/test_data/retrieved_data/' + city_name + '/'
	cf.validate_directory(out_path)
	output_file = open(out_path + city_name + '_' + lang + '_' + target_date + '.csv', 'wb')
	
	for f in test_data_files:
		input_file = open(test_datas_path + f)
		lines = input_file.readlines()
		#validate each sentence again.
		#write
		writeToFile(lines, output_file)
	output_file.close()
	return


if __name__ == '__main__':
	main()
