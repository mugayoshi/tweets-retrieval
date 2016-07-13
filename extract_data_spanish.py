import xml.etree.ElementTree as ET
import sys
import csv
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
	sentiment_value = []
	for gc in list(data):
		l = [x for x in gc.itertext()]
		sentiment_value = sentiment_value + l
	
	return sentiment_value

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
	for e in list(elem):
		tweet = ''
		sentiment_value = []
		for c in list(e):#c corresponds to a tweet data
			if c.tag == 'content':
				tweet = c.text
			elif c.tag == 'sentiments':
				sentiment_value = getSentimentDataList(c)

		if tweet is None or sentiment_value is None:
			continue
		elif len(tweet) == 0:
			continue
		line = '"' + tweet + '", ' + ' '.join(sentiment_value) + '\n'
		output_file.write(line.encode('utf-8'))#necessary to encode otherwise cannot write strings

	output_file.close()

if __name__ == "__main__":
		main()
