import sys
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.grid_search import GridSearchCV
import csv
from sklearn.ensemble import RandomForestClassifier

def extractLabelAndData(input_file):
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	for row in csv_reader:
		data.append(row[5])
		if row[0] == "4":
			labels.append(1) #positive
		elif row[0] == "2":
			labels.append(0.5) #neutral
		else:
			labels.append(0) #negative
	return (labels, data)

def main():
	#extract sentences (tweets)
	file_path = os.getcwd() + "/training.1600000.processed.noemoticon.csv"
	#file_path = os.getcwd() + "/csv_example.csv"

	if os.path.isfile(file_path) == False:
		print "the example file doesn't exist"
		quit()

	input_file = open(file_path, "rb")
	#make a list of labels and data
	labels = []
	tweets = []
	labels, tweets = extractLabelAndData(input_file)
	print 'extracting data has done'
	#generate a matrix of token counts
	count_vectorizer = CountVectorizer()
	feature_vectors = count_vectorizer.fit_transform(tweets)
	#learning by svm
	estimator = RandomForestClassifier()
	estimator.fit(feature_vectors, labels)
	print "learning has done"

if __name__ == "__main__":
	main()
