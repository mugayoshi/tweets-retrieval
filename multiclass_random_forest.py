from sklearn.ensemble import RandomForestClassifier
import csv
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

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
	"""
	file_train = '/home/nak/muga/twitter/training_data/de_sentiment_training_data.csv'
	file_test = '/home/nak/muga/twitter/training_data/de_sentiment_agree3_training_data.csv'
	label_train, data_train = getFeatureVecAndLabel(file_train)
	label_test, data_test = getFeatureVecAndLabel(file_test)
	"""
	file_input = '/home/nak/muga/twitter/train_data/de_sentiment_agree2_training_data.csv' #1720 data
	labels, feature_vec = getFeatureVecAndLabel(file_input)
	data_train, data_test, label_train, label_test = train_test_split(feature_vec, labels, test_size=0.2)
	print 'data extraction has done'
	scores = ['accuracy', 'precision', 'recall']
	for score in scores:
		print '\n' + '-'*50
		print score
		print '-'*50
		tuned_parameters = [{'n_estimators': [10, 30, 50, 70, 90, 110, 130, 150], 'max_features':['auto', 'sqrt', 'log2', None]}]
		clf = GridSearchCV(RandomForestClassifier(), param_grid=tuned_parameters, cv=3, scoring=score, n_jobs=-1)
		clf.fit(data_train, label_train)
		print clf.best_estimator_

		y_true, y_pred = label_test, clf.predict(data_test)
		print classification_report(y_true, y_pred)





if __name__ == "__main__":
	main()
