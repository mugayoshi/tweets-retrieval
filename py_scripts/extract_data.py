import sys
import os
import time
import csv
def main():
	output_file = open('refined_tweet_data_en.csv', 'ab')
	writer_output = csv.writer(output_file)
	corpus_file_path = "/home/nak/muga/annotated_corpus/twitter/senti140/training.1600000.processed.noemoticon.csv"

	input_file = open(corpus_file_path, "rb")
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	for row in csv_reader:
		try:
			row[5].decode('utf-8', 'strict')
		except:
			continue

		line_num = csv_reader.line_num
		line = [line_num]#adding line number to the row
		for item in row:
			line.append(item)
		
		writer_output.writerow(line)
		sys.stdout.write('\r%d' % line_num)
		sys.stdout.flush()
		time.sleep(0.01)
	print '\n'
	output_file.close()


if __name__ == "__main__":
	main()
