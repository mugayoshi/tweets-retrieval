import sys
import emoji

def find_tweets_with_emoji(key_face, emoji_dict, lang='en'):
	if lang == 'en':
		input_path_en = '/home/muga/twitter/classification_result/original_training_data/London/one_against_one/en/'
		input_filename_en = 'result_accuracy_London_en_20Nov_uniq_02Dec20161614.txt'
		input_file = open(input_path_en + input_filename_en)
	elif lang == 'de':
		input_path_de = '/home/muga/twitter/classification_result/original_training_data/Hamburg/one_against_one/de/'
		input_filename_de = 'result_accuracy_Hamburg_de_10Nov_uniq_01Dec20161426.txt'
		input_file = open(input_path_de + input_filename_de)
	elif lang == 'fr':
		input_path_fr = '/home/muga/twitter/classification_result/original_training_data/Paris/one_against_one/fr/'
		input_filename_fr = 'result_accuracy_Paris_fr_20Nov_uniq_01Dec20161350.txt'
		input_file = open(input_path_fr + input_filename_fr)
	elif lang == 'es':
		input_path_es = '/home/muga/twitter/classification_result/original_training_data/Barcelona/one_against_one/es/'
		input_filename_es = 'result_accuracy_Barcelona_es_04Nov_23Nov20161621.txt'
		input_file = open(input_path_es + input_filename_es)
	

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
	
	print '\n' + '*' * 10 + str(count) + ' tweets with ' + key_face + '*' * 10 + '\n'
	input_file.close()
	return count

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
		if len(sys.argv) > 2 and sys.argv[2] :
			lang = sys.argv[2]
		else:
			lang = 'en'
		key_list = find_keys(sys.argv[1], emoji_dict)
		if len(key_list) == 0:
			print 'no such key ' + sys.argv[1]
		num_result = 0
		for key in key_list:
			num_result += find_tweets_with_emoji(key, emoji_dict, lang)
		print '\n\n' + '#' * 10 + str(num_result) + ' for ' + sys.argv[1] + '#' * 10
	else:
		print 'keyword is necessary'
		quit()

if __name__ == '__main__':
	main()
