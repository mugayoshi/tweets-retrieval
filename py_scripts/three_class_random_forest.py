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

def classification(filename_train, filename_test):
	label_train, feat_vec_train, label_test, feat_vec_test = getFeatureVecsAndLabel(filename_train, filename_test)
	#data_train, data_test, label_train, label_test = train_test_split(feature_vec, labels, test_size=0.2)
	print 'data extraction has done'
	scores = ['accuracy', 'precision', 'recall']

	date = time.strftime('%d%b%Y%H%M')
	#out_file_name = filename_train.split('_')[0] + '_3class__result_' + date + '.txt'
	out_file_name = filename_train.split('/')[-1].split('.')[0] + '_3class_result_' + date + '.txt'
	out_file_path = "/home/nak/muga/twitter/classification_result/" + out_file_name #it is assumed this script is executed at twitter directory

	out = open(out_file_path, 'a')
	for score in scores:
		out.write('\n' + '-'*50)
		out.write(score)
		out.write('-'*50)
		tuned_parameters = [{'n_estimators': [10, 30, 50, 70, 90, 110, 130, 150], 'max_features':['auto', 'sqrt', 'log2', None]}]
		clf = GridSearchCV(RandomForestClassifier(), param_grid=tuned_parameters, cv=3, scoring=score, n_jobs=-1)
		clf.fit(feat_vec_train, label_train)
		#out.write(pp.pprint(clf.best_estimator_))
		print clf.best_estimator_

		y_true, y_pred = label_test, clf.predict(feat_vec_test)
		out.write(classification_report(y_true, y_pred))

		print 'loop for ' + score + ' has done\n' 
	
	out.close()
	print "classification of " + filename_train + " has done" 
	return

def extractTweetAndLabelForTrainData(filename):#from spanish data version
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	header = next(csv_reader)
	for row in csv_reader:
		try:
			row[1].decode('utf-8', 'strict') #depends on file
		except:
			continue
		data.append(row[1]) #depends on file
		if row[0] == "2": #neutral
			labels.append(2)
		elif row[0] == "1": #negative
			labels.append(1)
		elif row[0] == "0": #positive
			labels.append(0)
	
	return (labels, data)


def extractTweetAndLabelForTestData(filename):
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	non_utf_8 = 0
	header = next(csv_reader)
	for row in csv_reader:
		try:
			row[4].decode('utf-8', 'strict') #depends on file
		except:
			#print str(i) + ' ' + row[5] + ' contains non-utf-8 character'
			non_utf_8 = non_utf_8 + 1
			continue
		if row[1] == "3": #n/a isn't necessary in this script
			continue
		elif row[1] == "2": #neutral
			labels.append(2)
		elif row[1] == "1": #negative
			labels.append(1)
		elif row[1] == "0": #positive
			labels.append(0)
		data.append(row[4]) #depends on file
	#end of the for loop
	return (labels, data)

def getFeatureVecsAndLabel(file_train_data, file_test_data):#for both training and test data
	#generate a matrix of token counts
	labels_train, tweets_train = extractTweetAndLabelForTrainData(file_train_data)
	labels_test, tweets_test = extractTweetAndLabelForTestData(file_test_data)

	count_vectorizer_train = CountVectorizer()
	feat_vec_train = count_vectorizer_train.fit_transform(tweets_train)
	voc = count_vectorizer_train.get_feature_names()

	count_vectorizer_test = CountVectorizer(vocabulary=voc)
	feat_vec_test = count_vectorizer_test.fit_transform(tweets_test)

	return (labels_train, feat_vec_train, labels_test, feat_vec_test)

def main():
	if len(sys.argv) < 3:
		print 'please input a language and target date to specify the training data file'
		quit()
	lang = sys.argv[1]
	target_date = sys.argv[2]
	data_path = '/home/nak/muga/twitter/data_for_test2/'
	train_data = ''
	test_data = ''
	for f in os.listdir(data_path):
		if f.endswith('.csv') and f.startswith('trainingdata') and target_date in f:
			train_data = data_path + f
		elif f.endswith('.csv') and 'merge' in f and lang in f:
			test_data = data_path + f
	print 'train data: ' + train_data
	print 'test data: ' + test_data
	
	confirm = raw_input('it is going to process these files. is it okay ? (yes/no)' )
	if confirm == 'no' or confirm == 'No':
		print 'abort this program'
		quit()
	
	classification(train_data, test_data) 

if __name__ == "__main__":
	main()
