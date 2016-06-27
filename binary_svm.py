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
	print 'generating feature vectors has done'
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
	print 'Grid Search Cross Validation starts fitting ....'
	gscv.fit(feature_vectors, labels)
	print 'Fitting has done'
	svm_model = gscv.best_estimator_

	print svm_model

if __name__ == "__main__":
	main()
