import re
import os
import sys
import time
import common_functions as cf
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
	max_tweet = 100000
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
	for line in lines_of_tweet:
		#print line, str(len(line))
		if len(line) == 1 or line.startswith('Execution'):
			break
		tweet = line.split('\", ')[0] + '\"'
		created_at = '\"' + line.split('\", ')[1] + '\"'
		created_at = created_at.replace('\n', '')
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
			
		line = '"' + str(sentiment_value) + '", ' + tweet + ', ' + created_at + '\n'
		output_file.write(line.encode('utf-8'))#necessary to encode otherwise cannot write strings
		count += 1
		if count > max_tweet:
			break

	return

def eliminateEmoticons(tweet, emotion):
	#tweet is unicode type
	emoticon_list = cf.getEmoticonList(emotion)
	tweet_str = tweet.encode('utf-8')
	if len(emoticon_list) == 0:
		print 'the list is empty'
		quit()
	for word in tweet_str.split(' '):
		word = word.replace('\"', '') 
		word = word.replace('\n', '') 
		#word_str = word.encode('utf-8')
		for emoji in emoticon_list:
			if emoji in word:
				tweet = tweet.replace(emoji, '')
				#print 'replace', tweet
				#quit()
	#print tweet
	#quit()
	return  tweet

def main():
	if len(sys.argv) < 3:
		print 'the input must have emotion (pos, neg or neu) and target date of the text file)'
		quit()
	
	emotion = sys.argv[1]#pos, neg, neu
	target_date = sys.argv[2]
	if not emotion in ['pos', 'neg', 'neu']:
		print emotion + ' is wrong for input'
		quit()
	
	train_datas_path = '/home/muga/twitter/tweets_from_stream/training/'
	train_data_files = []
	for f in os.listdir(train_datas_path):
		if not target_date == '' and target_date in f and emotion in f:
			train_data_files.append(f)
			print 'append ' + f 
		elif target_date == '' and f.endswith('.txt') and emotion in f:
			train_data_files.append(f)
			print 'append ' + f 

	if len(train_data_files) == 0:
		print 'Not Found'
		quit()
	
	confirm = raw_input('it is going to process these files. is it okay ? (yes/no) ' )
	if not confirm.lower() in 'yes':
		print 'cancel'
		quit()

	out_path = '/home/muga/twitter/new_trainingdata/'
	#out_path = '/home/muga/twitter/new_trainingdata/debug/'
	cf.validate_directory(out_path, True)
	
	for f in train_data_files:
		input_file = open(train_datas_path + f)
		lines_of_tweet = input_file.readlines()
		#validate each sentence again.
		#in neutral tweets (news accounts) each tweet has URL therefore the URLs should be removed.
		#put affected value pos -> 0, neg -> 1, neu -> 2 ?
		#write
		lang = cf.find_lang(f)
		output_file = open(out_path + f.split('_')[0] + '_' + lang + '_' + emotion + '_train_data.csv', 'wb')
		writeToFile(lines_of_tweet, output_file, emotion)
		output_file.close()
	return


if __name__ == '__main__':
	main()
