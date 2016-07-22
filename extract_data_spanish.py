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

def main():
	argvs = sys.argv
	if len(argvs) < 2:
		print 'please input the output file name'
		quit()
	file_name = argvs[1]
	out_path = '/home/nak/muga/twitter/data_for_test2/'
	output_file = open(out_path + file_name, 'wb')

	#could choose train or test data
	#filepath = '/home/nak/muga/annotated_corpus/twitter/spanish/TASS/general-tweets-train-tagged.xml'
	filepath = '/home/nak/muga/annotated_corpus/twitter/spanish/TASS/general-tweets-test.xml'
	tree = ET.parse(filepath)
	elem = tree.getroot()
	for e in list(elem):#e corresponds to a tweet data
		tweet = ''
		sentiment_values = []
		affected_value = -1
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
		#print affected_value
		line = '"' + str(affected_value) + '", "' + tweet + '"\n'
		output_file.write(line.encode('utf-8'))#necessary to encode otherwise cannot write strings

	output_file.close()

if __name__ == "__main__":
		main()
