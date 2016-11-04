import os
import csv
from datetime import datetime
def validate_directory(path):
	if os.path.isdir(path) == False:
		print path + ' is not found or wrong. abort.'
		quit()
	return

def validate_language(lang):
	languages = ['en', 'fr', 'es', 'de', 'pt']
	if not lang in languages:
		print 'this language is not valid'
		quit()

	return True

def extract_tweet_from_test_data(filename):
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	data = []
	header = next(csv_reader)
	for row in csv_reader:
		try:
			row[0].decode('utf-8', 'strict') #depends on file
		except:
			continue
		data.append(row[0]) #depends on file

	if len(data) == 0:
		print 'no data'
		quit()
	else:
		print len(data)
			
	return data

def write_exec_time(start_time, output):
	end_time = datetime.now()
	exec_time = 'Execution time:%s' % (end_time - start_time)
	print exec_time
	output.write('\n\n\n' + exec_time + '\n')
	return
