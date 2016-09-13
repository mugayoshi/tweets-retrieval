import sys
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.grid_search import GridSearchCV
import csv
def extractLabels(input_file):
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	non_utf_8 = 0
	for row in csv_reader:
		try:
			row[5].decode('utf-8', 'strict')
		except:
			#print str(i) + ' ' + row[5] + ' contains non-utf-8 character'
			non_utf_8 = non_utf_8 + 1
			continue
		data.append(row[5])
		if row[0] == "4":
			labels.append(1)
		else:
			labels.append(0)
	return (labels, data)

def main():
	#extract sentences (tweets)
	print 'file name: ',
	file_name = raw_input()
	file_path = os.getcwd() + "/" + file_name
	if os.path.isfile(file_path) == False:
		print "the example file doesn't exist"
		quit()

	input_file = open(file_path, "rb")
	#make a list of labels and data
	lables = []
	tweets = []
	labels, tweets = extractLabels(input_file)
	print 'extracting data has done'

	#generate a matrix of token counts
	count_vectorizer = CountVectorizer()
	feature_vectors = count_vectorizer.fit_transform(tweets)
	
