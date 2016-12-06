import sys
import emoji

def find_tweets_with_emoji(key_face, emoji_dict):
	input_path = '/home/muga/twitter/classification_result/original_training_data/London/one_against_one/en/'
	input_filename = 'result_accuracy_London_en_20Nov_uniq_02Dec20161614.txt'
	input_file = open(input_path + input_filename)
	count = 0
	for line in input_file.readlines():
		#green_heart = emoji_dict[u':green_heart:']
		emoji_code = emoji_dict[key_face]
		"""
		print type(green_heart), type(line)
		quit()
		"""
		if emoji_code in line.decode('utf-8'):
			print line
			count += 1
	
	print 'there are ' + str(count) + ' tweets with ' + key_face
	input_file.close()

def find_keys(key_word, emoji_dict):
	uni_key_word = key_word.decode('utf-8')
	key_dict = []
	for key in emoji_dict.keys():
		if key_word in key:
			#print key.encode('utf-8'), emoji.emojize(key).encode('utf-8')
			#print "'" + key.encode('utf-8') + "'"
			key_dict.append(key)

	return key_dict


def main():
	emoji_dict = emoji.EMOJI_UNICODE
	if sys.argv[1]:
		key_dic = find_keys(sys.argv[1], emoji_dict)
		for key in key_dic:
			find_tweets_with_emoji(key,emoji_dict) 
	else:
		print 'keyword is necessary'
		quit()

if __name__ == '__main__':
	main()
