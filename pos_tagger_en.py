import sys
import os
import treetaggerwrapper
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.grid_search import GridSearchCV
def main():
	#read input file
	file_name = "example.txt"
	file_path = os.getcwd() + "/" + file_name
	if os.path.isfile(file_path) == False:
		print "the example file doesn't exist"
		quit()

	input = open(file_path, 'r')
	#generate a matrix of toke counts
	count_vectorizer = CountVectorizer()
	feature_vectors = count_vectorizer.fit_transform(input)
	vocabulary = count_vectorizer.get_feature_names()
	for word in vocabulary:
		print word
	
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

	gscv.fit(feature_vectors, [1,-1,1,1,1,-1,1,-1, 1)#test label
	svm_model = gscv.best_estimator_

	print svm_model

if __name__ == "__main__":
	main()
