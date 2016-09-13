import xml.etree.ElementTree as ET
import sys
import csv
import operator

def getSentimentDataList(data):
#each label string must be replace with number
	sentiment_values = []
	for gc in list(data):
		l = [x for x in gc.itertext()]
		for x in l:
			if x == 'PP' or x == 'P' or x == 'P+':
				sentiment_values.append('pos')
			elif x == 'N+' or x == 'N' or x == 'NN':
				sentiment_values.append('neg')
			elif x == 'NEU':
				sentiment_values.append('neu')
			elif x == 'NONE':
				sentiment_values.append('n/a')
	return sentiment_values

def getAffectedValue(sentiment_values, tweet):
	if len(sentiment_values) == 1:
		return getAffectedValueWithNum(sentiment_values[0])


	label_counts = {'pos': 0, 'neg': 0, 'neu': 0, 'na': 0}
	for x in sentiment_values:
		if x == 'pos':
			pos = label_counts['pos']
			label_counts['pos'] = pos + 1
		elif x == 'neg':
			neg = label_counts['neg']
			label_counts['neg'] = neg + 1
		elif x == 'neu':
			neu = label_counts['neu']
			label_counts['neu'] = neu + 1
		elif x == 'n/a':
			na = label_counts['na']
			label_counts['na'] = na + 1

	return getAffectedValueWithNum(max(label_counts, key=label_counts.get))#necessary to consider how to decide return value 
	
def getAffectedValueWithNum(affected_value):
	if affected_value == 'pos':
		return 0
	elif affected_value == 'neg':
		return 1
	elif affected_value == 'neu':
		return 2
	elif affected_value == 'na' or affected_value == 'n/a':
		return 3
	else:
		return -1
	
	return -1

def replaceURLAndUsername(tweet):
	tweet_original = tweet.encode('utf-8')
	tweet = tweet.encode('utf-8')
	modified = False
	
	for word in tweet.split(' '):
		if 'http' in word:
			tweet = tweet.replace(word, '~http')
			modified = True
		elif '@' in word:
			tweet = tweet.replace(word, '@user')
			modified = True
	"""
	if modified == True:
		print 'original\n' + tweet_original
		print '-> ' + tweet
	"""
	return tweet.decode('utf-8')

def getSentimentValue(data):
	prev_tag = ''
	for node in data.iter():
		if prev_tag == 'polarity' and node.tag == 'value':
			sentiment_value = node.text
			break
		prev_tag = node.tag
	
	if sentiment_value == 'PP' or sentiment_value == 'P' or sentiment_value == 'P+':
		return 0
	elif sentiment_value == 'N+' or sentiment_value == 'N' or sentiment_value == 'NN':
		return 1
	elif sentiment_value == 'NEU':
		return 2
	elif sentiment_value == 'NONE':
		return 3
	
	return -1


def main():
	argvs = sys.argv
	if len(argvs) < 3:
		print 'please input the output file name and option(-test or -train)'
		quit()
	file_name = argvs[1]
	option = argvs[2]
	out_path = '/home/nak/muga/twitter/data_for_test2/'
	output_file = open(out_path + file_name, 'wb')

	#could choose train or test data
	if option == '-train':
		filepath = '/home/nak/muga/annotated_corpus/twitter/spanish/TASS/general-tweets-train-tagged.xml'
	elif option == '-test':
		filepath = '/home/nak/muga/annotated_corpus/twitter/spanish/TASS/general-tweets-test-tagged.xml'

	tree = ET.parse(filepath)
	elem = tree.getroot()
	num_tweets = 0
	none_count = 0
	count = 0 #for counting how many tweets have multiple affected values
	for e in list(elem):#e corresponds to a tweet data
		tweet = ''
		sentiment_values = []
		sentiment_value = ''
		affected_value = -1
		for c in list(e):
			if c.tag == 'content':
				tweet = c.text
			elif c.tag == 'sentiments':
				sentiment_values = getSentimentDataList(c)
				sentiment_values = list(set(sentiment_values))
				sentiment_value = getSentimentValue(c)

		if tweet is None or sentiment_values is None:
			none_count = none_count + 1
			continue
		elif len(tweet) == 0:
			continue
		
		tweet = replaceURLAndUsername(tweet)
		if len(sentiment_values) > 1:
			count = count + 1

		line = '"' + str(sentiment_value) + '", "' + tweet + '"\n'
		output_file.write(line.encode('utf-8'))#necessary to encode otherwise cannot write strings
		"""
		affected_value = getAffectedValue(sentiment_values, tweet)
		for sentiment_val in sentiment_values:#wrtie the data to the output file each sentiment value
			affected_val = getAffectedValueWithNum(sentiment_val)
			line = '"' + str(affected_val) + '", "' + tweet + '"\n'
			output_file.write(line.encode('utf-8'))#necessary to encode otherwise cannot write strings
		"""
		num_tweets = num_tweets + 1

	output_file.close()
	print str(count) + ' tweets have several affected values out of ' + str(num_tweets) + ' tweets in ' + filepath.split('/')[-1]
	print 'there are ' + str(none_count) + ' Nones '

if __name__ == "__main__":
		main()
