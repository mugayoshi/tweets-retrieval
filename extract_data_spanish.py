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

def main():
	output_file = open('tweet_data_es.csv', 'ab')
	writer_output = csv.writer(output_file)

	filepath = '/home/nak/muga/annotated_corpus/twitter/spanish/TASS/general-tweets-train-tagged.xml'
	tree = ET.parse(filepath)
	elem = tree.getroot()
	for e in list(elem):
		tweet = ''
		sentiment_value = ''
		for c in list(e):
			if c.tag == 'content':
				tweet = c.text
			elif c.tag == 'sentiments':
				sentiment_value = getSentimentData(c)
		
		#quit()
		if tweet is None or sentiment_value is None:
			continue
		elif len(tweet) == 0:
			continue
		line = tweet + ', ' + sentiment_value 
		print 'tweet: ' + tweet
		print 'sentiment value: ' + sentiment_value

if __name__ == "__main__":
		main()
