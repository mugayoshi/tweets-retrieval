import sys
import os
import time
import csv
import random
def main():
	print 'number of data :',
	num_data = raw_input()
	num_sample = int(num_data) / 2
	output_file = open('random_picked_' + str(num_data) + 'data.csv', 'ab')
	writer_output = csv.writer(output_file)
	corpus_file_path = "/home/nak/muga/annotated_corpus/twitter/senti140/training.1600000.processed.noemoticon.csv"


	#0-799,999:positive
	#800,000-:negative
	random_positive = random.sample(xrange(800000), num_sample)
	random_negative = random.sample(xrange(800000, 1600000), num_sample)
	random_num = random_positive + random_negative
	input_file = open(corpus_file_path, "rb")
	#random_num = random_positive + random_negative
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	for row in csv_reader:
		try:
			row[5].decode('utf-8', 'strict')
		except:
			
			continue
		line_num = csv_reader.line_num
		if line_num in random_num:
			line = [line_num]
			for item in row:
				line.append(item)
			writer_output.writerow(line)
			sys.stdout.write('\r%d' % line_num)
			sys.stdout.flush()
			time.sleep(0.01)
			random_num.remove(line_num)
	print '\n'
	output_file.close()


if __name__ == "__main__":
	main()
