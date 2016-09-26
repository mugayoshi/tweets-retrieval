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
	if emotion == 'pos':
		sentiment_value = 0
	elif emotion == 'neg':
		sentiment_value = 1
	elif emotion == 'neu':
		sentiment_value = 2
	else:
		print emotion  + ' is invalid'
		quit()
	for tweet in lines_of_tweet:
		tweet = replaceURLAndUsername(tweet)
		if '~http' in tweet and emotion == 'neu':
			tweet = tweet.replace('~http', '')
		line = '"' + str(sentiment_value) + '", ' + tweet + '\n'
		output_file.write(line.encode('utf-8'))#necessary to encode otherwise cannot write strings

	return

def main():
	if len(sys.argv) < 3:
		print 'the input must have emotion (pos, neg or neu) and output file name)'
		quit()
	emotion = sys.argv[1]#pos, neg, neu
	file_name = sys.argv[2]
	if not emotion in ['pos', 'neg', 'neu']:
		print emotion + 'is wrong for input'
		quit()

	train_datas_path = '/home/nak/muga/twitter/py_scripts/tweets_from_stream/'
	train_data_files = []
	for f in os.listdir(train_datas_path):
		if f.endswith('.txt') and emotion in f:
			train_data_files.append(f)

	out_path = '/home/nak/muga/twitter/data_for_test2/'
	date = time.strftime("%d%b%Y%H%M")
	output_file = open(out_path + date + file_name, 'wb')

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
