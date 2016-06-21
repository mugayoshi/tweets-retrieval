import sys
import os
import treetaggerwrapper
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.grid_search import GridSearchCV
import csv
def extractLabels(input_file):
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	for row in csv_reader:
		data.append(row[5])
		if row[0] == "4":
			labels.append(1)
		else:
			labels.append(0)

		csv_reader.next()
	
	return (labels, data)

def main():
	#read input file
	#extract sentences (tweets)
	file_name = "csv_example.csv"
	file_path = os.getcwd() + "/" + file_name
	if os.path.isfile(file_path) == False:
		print "the example file doesn't exist"
		quit()

	input_file = open(file_path, "rb")
	#make a list of labels and data
	lables = []
	tweets = []
	labels, tweets = extractLabels(input_file)
	#generate a matrix of token counts
	count_vectorizer = CountVectorizer()
	feature_vectors = count_vectorizer.fit_transform(tweets)
	vocabulary = count_vectorizer.get_feature_names()
	#learning by svm
	svm_tuned_parameters = [
		{
			'kernel':['rbf'],
			'gamma':[2 ** n for n in range(-15, 3)],
			'C':[2 ** n for n in range(-5, 15)]
		}
	]
	
	gscv = GridSearchCV(
		svm.SVC(),
		svm_tuned_parameters,
		cv=5,#number of cross varidation
		n_jobs=1,# #of parallel thread
		verbose=3# output level of mid-result
	)

	#make a list of labels
	gscv.fit(tweets, labels)#test label
	svm_model = gscv.best_estimator_

	print svm_model

if __name__ == "__main__":
	main()
