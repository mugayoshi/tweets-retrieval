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

def classification(filename_train, filename_test):
	label_train, feat_vec_train, feat_vec_test = getFeatureVecsAndLabel(filename_train, filename_test)
	print 'data extraction has done'
	scores = ['accuracy', 'precision', 'recall']

	out_file_name = filename_test.split('/')[-1] + '.txt'
	city_name = sys.argv[1]
	out_file_path = "/home/muga/twitter/classification_result/random_forest/" + city_name + '/'
	cf.validate_directory(out_file_path)

	out = open(out_file_path + out_file_name, 'a')

	for score in scores:
		out.write('\n' + '-'*50)
		out.write(score)
		out.write('-'*50)
		tuned_parameters = [{'n_estimators': [10, 30, 50, 70, 90, 110, 130, 150], 'max_features':['auto', 'sqrt', 'log2', None]}]
		clf = GridSearchCV(RandomForestClassifier(), param_grid=tuned_parameters, cv=3, scoring=score, n_jobs=-1)
		clf.fit(feat_vec_train, label_train)
		print clf.best_estimator_

		y_pred = clf.predict(feat_vec_test)
		showResult(score, y_pred, out)
		print 'loop for ' + score + ' has done\n' 
	
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

def extractTweetAndLabelForTestData(filename):#from spanish data version
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	data = []
	header = next(csv_reader)
	for row in csv_reader:
		try:
			row[0].decode('utf-8', 'strict') #depends on file
		except:
			continue
		data.append(row[0]) #depends on file

	if len(data) == 0:
		print 'no data'
		quit()
	else:
		print len(data)
			
	return data


def extractTweetAndLabelForTrainData(filename):
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
		if row[1] == "2": #neutral
			continue
		elif row[1] == "1": #negative
			labels.append(1)
		elif row[1] == "0": #positive
			labels.append(0)
		data.append(row[4]) 
	#end of the for loop
	return (labels, data)

def extractSpanishData(filename):
	input_file = open(filename, 'rb')
	csv_reader = csv.reader(input_file, delimiter=",", quotechar='"')
	labels = []
	data = []
	non_utf_8 = 0
	header = next(csv_reader)
	for row in csv_reader:
		try:
			row[1].decode('utf-8', 'strict') #depends on file
		except:
			#print str(i) + ' ' + row[5] + ' contains non-utf-8 character'
			non_utf_8 = non_utf_8 + 1
			continue
		if row[0] == "2": #neutral
			labels.append(1)
		elif row[0] == "1": #negative
			labels.append(1)
		elif row[0] == "0": #positive
			labels.append(0)
		elif row[0] == "3":
			continue
		data.append(row[1]) 
	#end of the for loop
	return (labels, data)



def getFeatureVecsAndLabel(file_train_data, file_test_data):#for both training and test data
	#generate a matrix of token counts
	lang = sys.argv[2]
	if lang == 'es':
		labels_train, tweets_train = extractSpanishData(file_train_data)
	else:
		labels_train, tweets_train = extractTweetAndLabelForTrainData(file_train_data)
	tweets_test = extractTweetAndLabelForTestData(file_test_data)

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
	
	confirm = raw_input('it is going to process these files. is it okay ? (yes/no)' )
	if not confirm.lower() in 'yes':
		print 'abort this program'
		quit()
	
	classification(train_data, test_data) 

if __name__ == "__main__":
	main()
