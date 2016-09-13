import os
def counting(file_name):
	print 'counts the data of ' + file_name
	file_path = os.getcwd() + '/' + file_name
	if os.path.isfile(file_path) == False:
		print "this file doesn't exist"
		quit()
	
	input = open(file_path, 'r')
	s = input.readline()
	data = s.split(',')
	print 'length of this data ' + str(len(data))
	"""
	print data
	quit()
	"""
	positive = 0
	negative = 0
	for item in data:
		#print item,
		if item == " ": # check if it's empty
			continue
		i = int(item)
		if i == 1:
			positive = positive + 1
		elif i == 0:
			negative = negative + 1
	print file_name + ': positive ' + str(positive) + ', negative ' + str(negative)
def main():
	result_files = []
	for f in os.listdir(os.getcwd()):
		if 'tweets' in f and 'txt' in f and 'predict_result' in f:#collecting tweet data
			result_files.append(f)

	for f in result_files:
		counting(f)


if __name__ == "__main__":
	main()
