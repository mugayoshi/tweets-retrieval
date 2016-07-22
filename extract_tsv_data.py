import csv
import os
import sys
import pandas as pd
import shutil

def replaceSentimentValueWithNum(src, dest):
	csv_input = open(src, "rb")
	reader = csv.reader(csv_input)
	csv_output = open(dest, 'wb')
	writer = csv.writer(csv_output, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_ALL)
	#header = next(reader)
	for row in reader:
		if row[1] == 'positive':
			row[1] = 0
		elif row[1] == 'negative':
			row[1] = 1
		elif row[1] == 'neutral':
			row[1] = 2
		elif row[1] == 'na':
			row[1] = 3
		
		writer.writerow(row)
	csv_input.close()
	csv_output.close()

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

		#add "" to each item in a row
		src = '/home/nak/muga/twitter/' + output_file
		dest = '/home/nak/muga/twitter/train_data2/' + output_file
		replaceSentimentValueWithNum(src,dest)
		
		os.remove(src)
		
if __name__ == '__main__':
	main()
