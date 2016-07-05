import sys
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.grid_search import GridSearchCV
import csv
import time 
def writePredict(svm_model, feature_vectors, file_name, num_data):
	file_name = file_name.replace('.txt', '')
	
	results = svm_model.predict(feature_vectors)

	date = time.strftime("%d-%b-%y-%H-%M")
	output_file_name = "predict_result_" + date + '_' + file_name + '_with' + num_data + "data.txt"
	output_file = open(output_file_name, 'w')

	for item in results:
		output_file.write('%s, ' % item)

	output_file.close()
	
	return
	
def extractData(file_path):
	data = []
	with open(file_path) as f:
		for line in f:
			if "------- " in line:
				continue
			data.append(line)
	
	return data

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
			labels.append(1)#positive
		else:
			labels.append(0)#negative
	return (labels, data)

def main():
	#extract sentences (tweets)
	argvs = sys.argv
	if len(argvs) < 3:
		print 'please input file name of training data and the number of training data'
		quit()
	file_name = argvs[1]
	file_path = os.getcwd() + "/" + file_name
	if os.path.isfile(file_path) == False:
		print "the example file doesn't exist"
		quit()
	
	num_data = argvs[2]
	if not num_data in file_name:
		print "file name doesn't match the number of data"
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
	vocabulary_training_data = count_vectorizer.get_feature_names()
	
	print 'generating feature vectors has done'
	#learning by svm
	if len (argvs) == 4:
		kernel = argvs[3]
	else:
		kernel = 'rbf'
	svm_tuned_parameters = [
		{
			'kernel':[kernel],
			'gamma':[2 ** n for n in range(-15, 3)],
			'C':[2 ** n for n in range(-5, 15)]
		}
	]
	
	gscv = GridSearchCV(
		svm.SVC(),
		svm_tuned_parameters,
		cv=5,#number of cross varidation
		n_jobs=5,# #of parallel thread
		verbose=3# output level of mid-result
	)

	#make a list of labels
	print 'Grid Search Cross Validation starts fitting ....'
	gscv.fit(feature_vectors, labels)
	print 'Fitting has done'
	svm_model = gscv.best_estimator_

	print svm_model
	
	print '\nclassification starts\n'

	unknown_data_files = []
	for f in os.listdir(os.getcwd()):
		if 'tweets' in f and 'txt' in f and not 'result' in f:#collecting tweet data
			unknown_data_files.append(f)

	for unknown_data_file in unknown_data_files:
		file_path = os.getcwd() + "/" + unknown_data_file
		if os.path.isfile(file_path) == False:
			print unknown_data_file + " doesn't exist"
			quit()

		unknown_data = extractData(file_path)
		if len(unknown_data) < 1:
			print 'there is no data in ' + unknown_data_file
			continue
		count_vectorizer = CountVectorizer(vocabulary=vocabulary_training_data)
		feature_vectors_unknown_data = count_vectorizer.fit_transform(unknown_data)
		
		writePredict(svm_model, feature_vectors_unknown_data, unknown_data_file, num_data)
		print 'predicting ' + unknown_data_file + ' has done'

if __name__ == "__main__":
	main()
