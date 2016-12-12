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
import common_functions_general as cfg

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC, LinearSVC
from datetime import datetime
import itertools

def classification(filename_train, filename_test, strategy):
	label_train, feat_vec_train, feat_vec_test, tweets = getFeatureVecsAndLabel(filename_train, filename_test)
	print 'data extraction has done'
	scores = ['accuracy', 'precision_micro', 'recall_weighted', 'f1_micro']

	date = time.strftime("%d%b%Y%H%M")
	out_file_name = filename_test.split('/')[-1] + '_' + date + '_' + strategy +'.txt'
	out_file_name = out_file_name.replace('.csv', '')
	city_name = sys.argv[1]
	if 'emoji_replaced' in sys.argv:
		out_file_path = "/home2/muga/classification_result/emoji_replaced/" + city_name + "/" + strategy + '/'
	else:
		out_file_path = "/home2/muga/classification_result/" + city_name + "/" + strategy + '/'
	#out_file_path = "/home2/muga/classification_result/" + city_name + '/'
	cfg.validate_directory(out_file_path, True)
	lang = cfg.find_lang(filename_test.split('/')[-1])
	another_out_file_path = out_file_path + lang + '/'
	cfg.validate_directory(another_out_file_path, True)

	out = open(out_file_path + out_file_name, 'a')
	start_time = datetime.now()

	print '-' * 10 + strategy + ' ' + filename_test + '-' * 10
	for score in scores:
		if cfg.skip_parameter(score, strategy, lang):
			continue
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
		else:
			print strategy + ' is wrong'
			quit()
		clf.fit(feat_vec_train, label_train)
		print clf.best_estimator_

		y_pred = clf.predict(feat_vec_test)

		showResult(score, y_pred, out)
		writeResult(score, y_pred, tweets, out_file_name, another_out_file_path)
		print 'loop for ' + score + ' has done\n' 
	
	cfg.write_exec_time(start_time, out)
	out.close()
	print "classification of " + filename_test + " has done" 
	print '-' * 30
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

def writeResult(score, y_pred, tweets, filename_test, output_path):
	if not len(y_pred) == len(tweets):
		print 'the length of y_pred and tweets does not match'
		quit()
	out_file_name = 'result_' + score + '_' + filename_test
	out = open(output_path + out_file_name, 'a')

	for label, tweet in itertools.izip(y_pred, tweets):
		l = cfg.get_emotion_label(label)
		out.write(l + ', ' + tweet + '\n')
	out.close()




def getFeatureVecsAndLabel(file_train_data, file_test_data):#for both training and test data
	#generate a matrix of token counts
	lang = cfg.find_lang(file_test_data.split('/')[-1])
	labels_train, tweets_train = cfg.extract_train_data(file_train_data)
	
	tweets_test = cfg.extract_tweet_from_test_data(file_test_data)

	count_vectorizer_train = CountVectorizer()
	feat_vec_train = count_vectorizer_train.fit_transform(tweets_train)
	voc = count_vectorizer_train.get_feature_names()

	count_vectorizer_test = CountVectorizer(vocabulary=voc)
	feat_vec_test = count_vectorizer_test.fit_transform(tweets_test)

	return (labels_train, feat_vec_train, feat_vec_test, tweets_test)

def check_lang_file(filename, input_lang):
	languages = ['de', 'en', 'es', 'fr', 'pt']
	if not input_lang in languages:
		print 'wront input ' + input_lang
		quit()
	for w in filename.split('_'):
		if input_lang == w:
			#print 'check_lang_file ' + input_lang + ' ' + w
			return True
	return False

def main():
	if len(sys.argv) < 2:
		print 'please input city. And if neccesary enter the way of classification, language and  target date to specify the training data file'
		quit()

	if len(sys.argv) >= 3 and 'all' in sys.argv:
		strategy = 'all'
	elif sys.argv[-1] == 'one_against_one' or sys.argv[-1] == 'one_against_the_rest' or sys.argv[-1] == 'random_forest':
		strategy = sys.argv[-1]
	else:
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
	strategies = ['one_against_one', 'one_against_the_rest', 'random_forest'] 
	city_name = sys.argv[1]
	if len(sys.argv) >= 4 and 'all' in sys.argv:
		if sys.argv[2] in ['de', 'en', 'es', 'fr', 'pr']:
			lang = sys.argv[2]
			target_date = sys.argv[3]
		else:
			lang = ''
			target_date = sys.argv[2]
	elif len(sys.argv) > 3:
		lang = sys.argv[2]
		target_date = sys.argv[3]
		print 'target_date: ' + target_date
	else:
		lang = ''
		target_date = ''
	if 'emoji_replaced' in sys.argv:
		test_data_path = '/home2/muga/test_data/emoji_replaced/' + city_name + '/'
	else:
		test_data_path = '/home2/muga/test_data/' + city_name + '/'
	#test_data_path = '/home2/muga/test_data/' + city_name + '/'
	cfg.validate_directory(test_data_path)
	training_data_path = '/home2/muga/training_data/'
	train_data_dict = {}
	test_data_list = []#tweet data obtained from search API
	for f in os.listdir(test_data_path):
		if not 'uniq' in f:#test file should not contain duplicate lines
			continue
		if 'emoji_replaced' in sys.argv and not 'emoji_replaced' in f:
			continue
		if f.endswith('.csv') and f.startswith('') and target_date in f and lang in f:
			if lang and check_lang_file(f, lang):
					test_data_list.append(test_data_path + f)
			elif not lang:
				test_data_list.append(test_data_path + f)

	for f in os.listdir(training_data_path):
		if f.endswith('.csv') and 'merge' in f and 'uniq' in f:
			language = cfg.find_lang(f)
			train_data_dict[language] = training_data_path + f
			
		elif 'es' in f and 'training_data' in f and f.endswith('.csv'):
			language = cfg.find_lang(f)
			train_data_dict[language] = training_data_path + f

	if len(test_data_list) == 0:
		print 'Not Found'
		quit()

	print 'list of test data: '
	print '\n'.join(test_data_list)
	
	print 'list of training data: '
	for k in train_data_dict:
		print k, train_data_dict[k]

	if strategy == 'all':
		confirm = raw_input("it's going to do all classifications. Is it Okay ? (yes/no)")
	elif sys.argv[-1] == 'one_against_one' or sys.argv[-1] == 'one_against_the_rest' or sys.argv[-1] == 'random_forest':
		confirm = 'yes'
	else:
		confirm = raw_input('It is going to process these files with %s. Is it okay ? (yes/no)' % strategy)
	if not confirm.lower() in 'yes':
		print 'cancel'
		quit()
	"""
	print 'strategy = ' + strategy + ', '.join(sys.argv)
	quit()
	"""
	for test_data in test_data_list:
		if lang:
			language = lang
		else:
			language = cfg.find_lang(test_data.split('/')[-1])
		train_data = train_data_dict[language]
		print 'train data: ' + train_data
		print 'test on ' + test_data
		if strategy == 'all':
			for s in strategies:
				classification(train_data, test_data, s) 
		else:
			classification(train_data, test_data, strategy) 

if __name__ == "__main__":
	main()
