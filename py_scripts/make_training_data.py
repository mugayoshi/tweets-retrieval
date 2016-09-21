import os
def main():
	
	train_datas_path = '/home/nak/muga/twitter/py_scripts/tweets_from_stream/'
	for f in os.listdir(train_datas_path):
		if f.endswith('.txt') and 'TIME' in f:
			input_file = open('/home/nak/muga/twitter/py_scripts/tweets_from_stream/' + f)
			#lines_of_tweet = input_file.readlines()
			count = 0
			for line in input_file.readlines():
				print line
				count += 1
				if count == 5:
					quit()
	
	#validate each sentence again.
	#replace URL and @XXX with constant string
	#in neutral tweets (news accounts) each tweet has URL therefore the URLs should be removed.
	#put affected value pos -> 0, neg -> 1, neu -> 2 ?
	#write



if __name__ == '__main__':
	main()
