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
	out_file_name = filename.split('/')[-1].split('_')[0] + '_classsification_result_' + date + '.txt'
	out_file_path = os.getcwd() + "/classification_result/" + out_file_name #this script is assumed to be  executed at twitter directory

	out = open(out_file_path, 'a')
	#pp = pprint.PrettyPrinter(indent=4)
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
		#print classification_report(y_true, y_pred, )
		out.write(classification_report(y_true, y_pred))

		print 'loop for ' + score + ' has done\n' 
	
	out.close()
	print "classification of " + filename + " has done" 
	return

def extractTweetAndLabel(filename):
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	non_utf_8 = 0
	header = next(csv_reader)
	for row in csv_reader:
		try:
			#row[5].decode('utf-8', 'strict')
			row[4].decode('utf-8', 'strict') #depends on file
		except:
			#print str(i) + ' ' + row[5] + ' contains non-utf-8 character'
			non_utf_8 = non_utf_8 + 1
			continue
		#data.append(row[5])
		"""print row[4] + ' passed'
		quit()"""
		data.append(row[4]) #depends on file
		if row[1] == "3": #n/a
			labels.append(3)
		elif row[1] == "2": #neutral
			labels.append(2)
		elif row[1] == "1": #negative
			labels.append(1)
		elif row[1] == "0": #positive
			labels.append(0)
	
	return (labels, data)

def getFeatureVecAndLabel(filename):
	#generate a matrix of token counts
	labels, tweets = extractTweetAndLabel(filename)
	count_vectorizer = CountVectorizer()
	feature_vectors = count_vectorizer.fit_transform(tweets)
	#vocabulary_training_data = count_vectorizer.get_feature_names()

	return (labels, feature_vectors)

def main():

	train_datas_path = '/home/nak/muga/twitter/data_for_test2/'
	train_datas = []
	for f in os.listdir(train_datas_path):
		if f.endswith('.csv') and 'merge' in f:
			train_datas.append(train_datas_path + f)
	
	for f in train_datas:
		classification(f)


if __name__ == "__main__":
	main()
