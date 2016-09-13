from sklearn.ensemble import RandomForestClassifier
import csv
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_score, recall_score, f1_score
import os
import sys
import time

def classification(filename):
	labels, feature_vec = getFeatureVecAndLabel(filename)
	data_train, data_test, label_train, label_test = train_test_split(feature_vec, labels, test_size=0.2)
	print 'data extraction has done'
	scores = ['accuracy', 'precision', 'recall']

	date = time.strftime('%Y%m%d-%H%M%S')
	#file_data_str = filename.split('/')[-1].split('.')[0]
	out_file_name = filename.split('/')[-1].split('.')[0] + '_classsification_result_' + date + '.txt'
	out_file_path = os.getcwd() + "/classification_result/" + out_file_name #this script is assumed to be  executed at twitter directory

	out = open(out_file_path, 'a')
	for score in scores:
		out.write('\n' + '-'*50)
		out.write(score)
		out.write('-'*50)
		tuned_parameters = [{'n_estimators': [10, 30, 50, 70, 90, 110, 130, 150], 'max_features':['auto', 'sqrt', 'log2', None]}]
		clf = GridSearchCV(RandomForestClassifier(), param_grid=tuned_parameters, cv=3, scoring=score, n_jobs=-1)
		clf.fit(data_train, label_train)
		#out.write(pp.pprint(clf.best_estimator_))
		print clf.best_estimator_

		y_true, y_pred = label_test, clf.predict(data_test)
		out.write(classification_report(y_true, y_pred))

	
	out.close()
	print "classification  of " + out_file_name + " has done  " 
	return

def extractTweetAndLabel(filename):
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	header = next(csv_reader)
	for row in csv_reader:
		try:
			row[1].decode('utf-8', 'strict') #depends on file
		except:
			#print str(i) + ' ' + row[5] + ' contains non-utf-8 character'
			continue
		#data.append(row[5])
		data.append(row[1]) #depends on file
		if row[0] == "3": #n/a
			labels.append(3)
		elif row[0] == "2": #neutral
			labels.append(2)
		elif row[0] == "1": #negative
			labels.append(1)
		elif row[0] == "0": #positive
			labels.append(0)
	
	return (labels, data)

def getFeatureVecAndLabel(filename):
	#generate a matrix of token counts
	labels, tweets = extractTweetAndLabel(filename)
	count_vectorizer = CountVectorizer()
	feature_vectors = count_vectorizer.fit_transform(tweets)

	return (labels, feature_vectors)

def main():

	path = '/home/nak/muga/twitter/data_for_test2/'
	
	for f in os.listdir(path):
		if f.endswith('.csv') and 'esp_test' in f and 'uno' in f:#keywords for selecting files change depending on what you can check  etc
			#label_train, data_train = getFeatureVecAndLabel(path + f)
			classification(path + f)

		"""elif f.endswith('.csv') and 'esp' in f and 'test' in f:
			label_test, data_test = getFeatureVecAndLabel(path + f)
		
	classification(label_train, label_test, data_train, data_test)"""

	print 'Done !'

if __name__ == "__main__":
	main()
