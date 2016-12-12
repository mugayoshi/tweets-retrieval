import emoji
import csv
import common_functions_general as cfg
import os
import sys
def make_dictionary(lang='en'):

	dict_file = '/home/muga/twitter/emoji_dict_all.csv'
	
	input_file = open(dict_file, 'rU')
	csv_reader = csv.reader(input_file, delimiter=",")
	emoji_descp_dict = {}
	#header = next(csv_reader)
	for row in csv_reader:
		#print row[0], row[1]
		#print ', '.join(row)
		#data.append(row[0]) #depends on file
		if not ':' in row[0]:
			continue
		if lang == 'en':
			emoji_descp_dict[row[0]] = row[1]
		elif lang == 'fr':
			emoji_descp_dict[row[0]] = row[2]
		elif lang == 'de':
			emoji_descp_dict[row[0]] = row[3]
		elif lang == 'es':
			emoji_descp_dict[row[0]] = row[4]
		elif lang == 'pt':
			emoji_descp_dict[row[0]] = row[5]
		
	"""
	for k in emoji_descp_dict:
		print k, emoji_descp_dict[k]
	quit()
	"""

	return emoji_descp_dict

def replace_emoji_with_str(emoji_descp_dict, test_data, outfile):
	emoji_dict = emoji.EMOJI_UNICODE
	valid_keys = []
	for key in emoji_dict.keys():
		if key in emoji_descp_dict.keys():
			valid_keys.append(key)

	for line in test_data.readlines():
		output_line = line
		changed = False
		for key in valid_keys:
			emoji_code = emoji_dict[key]
			emoji_descp = emoji_descp_dict[key]
			#print 'emoji code ' + str(type(emoji_code)) + ' line ' + str(type(line.decode('utf-8')))
			try:
				if emoji_code in line.decode('utf-8'):
					replaced_with = ' { ' + emoji_descp + ' } ' 
					output_line = output_line.replace(emoji_code.encode('utf-8'), replaced_with)
					#print 'replaced ' + key.encode('utf-8') + ' ' + emoji_code.encode('utf-8') + ' ' + emoji_descp
					changed = True
			except:
				continue
		"""
		if changed:
			print line + ' ---> ' + output_line
		"""
		outfile.write(output_line)
	return

def obtain_language(lang):
	if lang == 'en':
		return 'ENGLISH'
	elif lang == 'fr':
		return 'FRENCH'
	elif lang == 'de':
		return 'GERMAN'
	elif lang == 'es':
		return 'SPANISH'
	elif lang == 'pt':
		return 'PORTUGESE'
	else:
		return ''

def main():
	if len(sys.argv) < 3:
		print 'must input city name and language if necessary.'
		quit()
	city = sys.argv[1]
	lang = sys.argv[2]
	if len(sys.argv) >= 4:
		target_date = sys.argv[3]
	else:
		target_date = ''
	emoji_descp_dict = make_dictionary(lang)
	test_data_path = '/home/muga/twitter/test_data/retrieved_data/' + city + '/'
	test_data_list = []
	for f in os.listdir(test_data_path):
		lang_in_file = '_' + lang + '_'
		if lang_in_file in f and city in f and target_date in f:
			test_data_list.append(f)
			print 'found ' + f
	if len(test_data_list) == 0:
		print 'Not Found'
		quit()
	print '\nTarget Language is ' + obtain_language(lang) + '\n'
	#test_data = test_data_path + 'London_en_20Nov_uniq.csv'
	out_path = '/home/muga/twitter/test_data/emoji_replaced/' + city + '/'
	cfg.validate_directory(out_path, True)
	for f in test_data_list:
		out_filename = 'emoji_replaced_' + f
		print 'starts replacing ' + f
		input_file = open(test_data_path + f, 'r')
		output_file = open(out_path + out_filename, 'w')
		replace_emoji_with_str(emoji_descp_dict, input_file, output_file)
		input_file.close()
		output_file.close()
		print 'Replacing ' + f + ' has changed'

	return

if __name__ == "__main__":
	main()

