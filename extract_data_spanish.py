import xml.etree.ElementTree as ET
import sys
import csv
import operator

def getSentimentData(data):
	sentiment_value = ''
	for gc in list(data):
		l = [x for x in gc.itertext()]
		value = ''
		for el in l:
			value += el + ' '
		value += ', '
		sentiment_value += value
	return sentiment_value

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

def getAffectedValue(sentiment_values):
	if len(sentiment_values) == 1:
		return sentiment_values[0]
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
	"""print label_counts
	quit()"""
	return max(label_counts, key=label_counts.get)#necessary to consider how to decide return value 


def main():
	argvs = sys.argv
	if len(argvs) < 2:
		print 'please input the output file name'
		quit()
	file_name = argvs[1]
	output_file = open(file_name, 'wb')
	#output_file = open('tweet_data_es.csv', 'wb')

	filepath = '/home/nak/muga/annotated_corpus/twitter/spanish/TASS/general-tweets-train-tagged.xml'
	tree = ET.parse(filepath)
	elem = tree.getroot()
	for e in list(elem):#e corresponds to a tweet data
		tweet = ''
		sentiment_values = []
		for c in list(e):
			if c.tag == 'content':
				tweet = c.text
			elif c.tag == 'sentiments':
				sentiment_values = getSentimentDataList(c)

		if tweet is None or sentiment_values is None:
			continue
		elif len(tweet) == 0:
			continue
		affected_value = getAffectedValue(sentiment_values)
		#line = '"' + tweet + '", ' + ' '.join(sentiment_values) + '\n'
		line = '"' + tweet + '", ' + affected_value + '\n'
		output_file.write(line.encode('utf-8'))#necessary to encode otherwise cannot write strings

	output_file.close()

if __name__ == "__main__":
		main()
