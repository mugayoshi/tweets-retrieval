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
def classification(filename, strategy):
	labels, feature_vec = getFeatureVecAndLabel(filename)
	data_train, data_test, label_train, label_test = train_test_split(feature_vec, labels, test_size=0.2)
	
	print 'data extraction has done'
	scores = ['accuracy', 'precision', 'recall']

	date = time.strftime('%d%b%Y%H%M')
	out_file_name = filename.split('/')[-1].split('.')[0] + '_' + date+ '.txt'
	out_file_path = "/home/muga/twitter/classification_result/classifier_evaluation/" + strategy + "/"
	cf.validate_directory(out_file_path)

	out = open(out_file_path + out_file_name, 'a')
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
		elif strategy == 'random_forest':
			tuned_parameters = [{'n_estimators': [10, 30, 50, 70, 90, 110, 130, 150], 'max_features':['auto', 'sqrt', 'log2', None]}]
			clf = GridSearchCV(RandomForestClassifier(), param_grid=tuned_parameters, cv=3, scoring=score, n_jobs=-1)
		clf.fit(data_train, label_train)
		print clf.best_estimator_

		y_true, y_pred = label_test, clf.predict(data_test)
		out.write(classification_report(y_true, y_pred))

		print 'loop for ' + score + ' has done\n' 
	
	out.close()
	print "classification of " + filename + " has done" 
	return

def extractTweetAndLabel(filename):#from spanish data version
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	header = next(csv_reader)
	for row in csv_reader:
		try:
			row[1].decode('utf-8', 'strict') #depends on file
			text = row[1].decode('utf-8', 'strict') 
		except:
			continue
		data.append(row[1]) #depends on file
		if len(text) == 0:
			print 'no length of text. abort this program' 
			quit()
		if row[0] == "2": #neutral
			labels.append(2)
		elif row[0] == "1": #negative
			labels.append(1)
		elif row[0] == "0": #positive
			labels.append(0)
	
	return (labels, data)

def getFeatureVecAndLabel(filename):#for both training and test data
	#generate a matrix of token counts
	lang = sys.argv[1]
	if lang == 'es':
		labels, tweets = extractSpanishData(filename)
	else:
		labels, tweets = extractTweetAndLabelForTrainData(filename)
	count_vectorizer = CountVectorizer()
	feature_vectors = count_vectorizer.fit_transform(tweets)

	"""
	labels, tweets = extractTweetAndLabel(filename)
	count_vectorizer = CountVectorizer()
	feature_vectors = count_vectorizer.fit_transform(tweets)
	"""

	return (labels, feature_vectors)
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

def main():
	if len(sys.argv) < 2:
		print 'please input a language and target date to specify the training data file'
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
	lang = sys.argv[1]
	input_data_path = '/home/muga/twitter/original_trainingdata/'
	evaluated_data = ''
	for f in os.listdir(input_data_path):
		if f.endswith('.csv') and 'merge' in f and lang in f:
			evaluated_data = input_data_path + f
			break
		if lang == 'es' and 'training_data' in f and lang in f:
			evaluated_data = input_data_path + f
			break
	print 'train data: ' + evaluated_data
	
	confirm = raw_input('it is going to process this file with %s. is it okay ? (yes/no)' % strategy)
	if confirm == 'no' or confirm == 'No':
		print 'cancel'
		quit()
	
	classification(evaluated_data, strategy) 

if __name__ == "__main__":
	main()
