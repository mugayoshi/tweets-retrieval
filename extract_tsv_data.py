import os
import sys
import pandas as pd

def replaceWithNum(filename, sentiment_str, sentiment_value):
	with open(filename) as f:
		s = f.read()
		if sentiment_str not in s:
			print sentiment_str + ' is not found'
			return
	
	with open(filename, 'w') as f:
		s = s.replace(sentiment_str, sentiment_value)
		f.write(s)
	
	return

def main():
	argvs = sys.argv
	if len(argvs) < 2:
		print 'please input the output file name'
		quit()
	output_file = argvs[1]
	#output_file = open(file_name, 'wb')
	corpus_file_path = "/home/nak/muga/annotated_corpus/twitter/SentimentDatasetDaiLabor/de_sentiment_agree2.tsv"
	input_file = pd.read_csv(corpus_file_path, delimiter='\t')
	input_file.to_csv(output_file)
	
	replaceWithNum(output_file, 'positive', '0')
	replaceWithNum(output_file, 'negative', '1')
	replaceWithNum(output_file, 'neutral', '2')
	replaceWithNum(output_file, 'na', '3')
	

if __name__ == '__main__':
	main()
