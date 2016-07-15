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
	corpus_path = '/home/nak/muga/annotated_corpus/twitter/SentimentDatasetDaiLabor/'
	tsv_files = []
	for f in os.listdir(corpus_path):
		if f.endswith('.tsv'):
			tsv_files.append(f)
	for f in tsv_files:
		file_path = corpus_path + f
		input_file = pd.read_csv(file_path, delimiter='\t')
		output_file = f.split('.')[0] + '_training_data.csv'
		input_file.to_csv(output_file)
		
		replaceWithNum(output_file, 'positive', '0')
		replaceWithNum(output_file, 'negative', '1')
		replaceWithNum(output_file, 'neutral', '2')
		replaceWithNum(output_file, 'na', '3')
	
if __name__ == '__main__':
	main()
