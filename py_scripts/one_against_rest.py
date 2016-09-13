from sklearn.multiclass import OneVsRestCLassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

def main():
	#read data
	#setting parameters
	C = 1
	kernel = 'rbf'
	gamma  = 0.01

	estimator = SVC(C=C, kernel=kernel, gamma=gamma)
	classifier = OneVsRestClassifier(estimator)
	classifier.fit(train_x, train_y)
	pred_y = classifier.predict(test_x)

	print 'accuracy score: {:.5f}'.format(accuracy_score(test_y, pred_y))
if __name__ == "__main__":
	main()
