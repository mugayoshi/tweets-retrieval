import sys
sys.path.append('/home/nak/muga/libsvm-3.21/python')
from svmutil import *
from svm import *

def main():
	input_data = [[1,2,3], [4,5,6], [7,8,9] ]
	label1 = [-1.-1.-1]
	prob = svm_problem(label1, data1)
	param = svm_parameter('-s 0 -t 0')
	m = svm_trian(prob, param) #learning
	result = svm_predict( [-1,-1], [[33,22], [1000, 100] ], m ) #unknown data

#write out the model to a file if you want to check the model afterwards
	svm_save_model('test.model', m)
	print result[0], result[1], result[2]


if __name__ == "__main__":
	main()
