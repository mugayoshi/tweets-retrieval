import csv
import os
import sys
import pandas as pd
import shutil

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
		
		src = '/home/nak/muga/twitter/' + output_file
		dest = '/home/nak/muga/twitter/train_data/' + output_file
		#add "" to each item in a row
		csv_input = open(src, "rb")
		reader = csv.reader(csv_input)
		csv_output = open(dest, 'wb')
		writer = csv.writer(csv_output, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_ALL)
		header = next(reader)
		for row in reader:
			writer.writerow(row)
		csv_input.close()
		csv_output.close()
		os.remove(src)
		
if __name__ == '__main__':
	main()
