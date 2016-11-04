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
import common_functions as cf

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC, LinearSVC
from datetime import datetime

def classification(filename_train, filename_test, strategy):
	label_train, feat_vec_train, feat_vec_test = getFeatureVecsAndLabel(filename_train, filename_test)
	print 'data extraction has done'
	scores = ['accuracy', 'precision', 'recall']

	out_file_name = filename_test.split('/')[-1] + '.txt'
	city_name = sys.argv[1]
	out_file_path = "/home/muga/twitter/classification_result/" + strategy + "/" + city_name + '/'
	cf.validate_directory(out_file_path)

	out = open(out_file_path + out_file_name, 'a')
	start_time = datetime.now()

	for score in scores:
		out.write('\n' + '-'*50)
		out.write(score)
		out.write('-'*50)

		if strategy == 'one_against_the_rest':
			tuned_parameters = {'C': [1, 10, 100, 1000], 'tol':[1e-3, 1e-4], 'multi_class': ['ovr', 'crammer_singer'] }
			clf = GridSearchCV(LinearSVC(C=1), param_grid=tuned_parameters, cv=5, scoring=score, n_jobs=-1)
		elif strategy == 'one_against_one':
			tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}, {'kernel':['linear'], 'C': [1, 10, 100, 1000] }]
			clf = GridSearchCV(SVC(C=1), param_grid=tuned_parameters, cv=5, scoring=score, n_jobs=-1)
		elif strategy = 'random_forest':
			tuned_parameters = [{'n_estimators': [10, 30, 50, 70, 90, 110, 130, 150], 'max_features':['auto', 'sqrt', 'log2', None]}]
			clf = GridSearchCV(RandomForestClassifier(), param_grid=tuned_parameters, cv=3, scoring=score, n_jobs=-1)
		else:
			print strategy + ' is wrong'
			quit()
		clf.fit(feat_vec_train, label_train)
		print clf.best_estimator_

		y_pred = clf.predict(feat_vec_test)

		showResult(score, y_pred, out)
		print 'loop for ' + score + ' has done\n' 
	
	cf.write_exec_time(start_time, out)
	out.close()
	print "classification of " + filename_train + " has done" 
	return

def showResult(score, y_pred, out):
	pos = 0
	neg = 0
	neu = 0
	total = len(y_pred)
	for label in y_pred:
		if label == 0:
			pos += 1
		elif label == 1:
			neg += 1
		elif label == 2:
			neu += 1
		else:
			print 'Error: label is ' + label
			quit()
	
	result =  score + '\npositive: ' + str(pos) + ' negative: ' + str(neg) + ' neutral: ' + str(neu) + ' out of ' + str(total) + ' tweets\n'
	out.write(result)
	print result

	return


def extractTweetAndLabelForTrainData(filename):
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	non_utf_8 = 0
	header = next(csv_reader)
	pos = 0
	neg = 0
	neu = 0
	n_a = 0
	for row in csv_reader:
		try:
			row[4].decode('utf-8', 'strict') #depends on file
		except:
			#print str(i) + ' ' + row[5] + ' contains non-utf-8 character'
			non_utf_8 = non_utf_8 + 1
			continue
		if row[1] == "2": #neutral
			labels.append(2)
			neu+= 1
		elif row[1] == "1": #negative
			labels.append(1)
			neg += 1
		elif row[1] == "0": #positive
			labels.append(0)
			pos += 1
		elif row[1] == "3":
			n_a += 1
			continue
		data.append(row[4]) 
	#end of the for loop
	print 'training data positive: ' + str(pos) + ' negative: ' + str(neg) + ' neutral: ' + str(neu) + ' n/a: ' + str(n_a)
	return (labels, data)

def extractSpanishData(filename):#for training data
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	non_utf_8 = 0
	header = next(csv_reader)
	pos = 0
	neg = 0
	neu = 0
	n_a = 0
	for row in csv_reader:
		try:
			row[1].decode('utf-8', 'strict') #depends on file
		except:
			#print str(i) + ' ' + row[5] + ' contains non-utf-8 character'
			non_utf_8 = non_utf_8 + 1
			continue
		if row[0] == "2": #neutral
			labels.append(1)
			neu += 1
		elif row[0] == "1": #negative
			labels.append(1)
			neg += 1
		elif row[0] == "0": #positive
			labels.append(0)
			pos += 1
		elif row[0] == "3":
			n_a += 1
			continue
		data.append(row[1]) 
	#end of the for loop
	print 'training data positive: ' + str(pos) + ' negative: ' + str(neg) + ' neutral: ' + str(neu) + ' n/a: ' + str(n_a)
	return (labels, data)



def getFeatureVecsAndLabel(file_train_data, file_test_data):#for both training and test data
	#generate a matrix of token counts
	lang = sys.argv[2]
	if lang == 'es':
		labels_train, tweets_train = extractSpanishData(file_train_data)
	else:
		labels_train, tweets_train = extractTweetAndLabelForTrainData(file_train_data)
	tweets_test = cf.extract_tweet_from_test_data(file_test_data)

	count_vectorizer_train = CountVectorizer()
	feat_vec_train = count_vectorizer_train.fit_transform(tweets_train)
	voc = count_vectorizer_train.get_feature_names()

	count_vectorizer_test = CountVectorizer(vocabulary=voc)
	feat_vec_test = count_vectorizer_test.fit_transform(tweets_test)

	return (labels_train, feat_vec_train, feat_vec_test)

def main():
	if len(sys.argv) < 3:
		print 'please input city name,  language and target date to specify the training data file'
		quit()

	clf_strategy  = raw_input('One against One (0), One against The Rest (1) or Random Forest (2)  ----> ' )
	if clf_strategy == str(0):
		strategy = 'one_against_one'
	elif clf_strategy == str(1):
		strategy = 'one_against_the_rest'
	elif clf_strategy == str(2):
		strategy = 'random_forest'
	else:
		print 'wrong input ' + clf_strategy
		quit()
	city_name = sys.argv[1]
	lang = sys.argv[2]
	target_date = sys.argv[3]
	test_data_path = '/home/muga/twitter/test_data/retrieved_data/' + city_name + '/'
	cf.validate_directory(test_data_path)
	training_data_path = '/home/muga/twitter/original_trainingdata/'
	train_data = ''
	test_data = ''#tweet data obtained from search API
	for f in os.listdir(test_data_path):
		if f.endswith('.csv') and f.startswith('') and target_date in f and lang in f:
			test_data = test_data_path + f
			break
	for f in os.listdir(training_data_path):
		if f.endswith('.csv') and 'merge' in f and lang in f:
			train_data = training_data_path + f
			break
		if lang == 'es' and 'training_data' in f and lang in f:
			train_data = training_data_path + f
			break

	print 'train data: ' + train_data
	print 'test data: ' + test_data
	
	confirm = raw_input('It is going to process these files with %s. Is it okay ? (yes/no)' % strategy)
	if not confirm.lower() in 'yes':
		print 'cancel'
		quit()
	
	classification(train_data, test_data, strategy) 

if __name__ == "__main__":
	main()
