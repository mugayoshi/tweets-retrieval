import os
import csv

def main():
	pos_file = open('positive_tweets.csv', 'ab')
	neu_file = open('neutral_tweets.csv', 'ab')
	neg_file = open('negative_tweets.csv', 'ab')
	pos_writer = csv.writer(pos_file)
	neu_writer = csv.writer(neu_file)
	neg_writer = csv.writer(neg_file)

	file_path = "/home/nak/muga/annotated_corpus/twitter/senti140/training.1600000.processed.noemoticon.csv"
	if os.path.isfile(file_path) == False:
		print "the example file doesn't exist"
		quit()

	input_file = open(file_path, "r")
	
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	for row in csv_reader:
		if row[0] == "4":
			pos_writer.writerow(row) #positive
		elif row[0] == "2":
			neu_writer.writerow(row) #neutral
		else:
			neg_writer.writerow(row) #negative

	pos_file.close()
	neu_file.close()
	neg_file.close()

if __name__ == "__main__":
	main()
