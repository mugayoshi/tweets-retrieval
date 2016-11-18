import twitter
import json
import sys
import os
import common_functions as cf
import time
def validate_area(country, searched):
	if searched == 'US':
		searched = 'United States'
	elif searched == 'UK':
		searched = 'United Kingdom'
	if country == searched:
		return True
	else:
		return False
def main():
	twitter_api = cf.authentication_twitter(sys.argv[-1])
	argvs = sys.argv
	searched_country = ''
	if len(argvs) > 1:
		cityname = argvs[1]
		if len(sys.argv) > 2 and sys.argv[2].isalpha() == False:
			wait_time = int(sys.argv[2])
			print 'Please wait for ' + sys.argv[2] + ' minutes'
			time.sleep(60*wait_time + 5)

		if 't' in argvs[2]:#argvs[2] has to contain 't' to make 'non_city_name' true.
			non_city_name = True
			print 'non_city_name is True'
		else:
			non_city_name = False
	accuracy = 10000
	if cityname:
		result = twitter_api.geo.search(query=cityname)
	else:
		print cityname + ' ' + granularity + ' ' + latitude + ' ' + longtitude
		quit()

	places = result['result']['places']
	place_id_dict = {}
	for place in places:
		place_full_name = place['full_name']
		place_name = place['name']
		place_id = place['id']
		country = place['country']
		if searched_country and validate_area(country, searched_country) == False:
			print 'fullname: ' + place_full_name + ', country: ' + country
			continue
		place_list = [place_full_name, place_name]
		place_id_dict[place_id] = place_list

	if non_city_name:
		out_file_path = "/home/muga/twitter/place_id_data/others/"
	else:
		cityname = cityname.replace(' ','')
		out_file_path = "/home/muga/twitter/place_id_data/" + cityname + "/"
	file_name = "placeid_" + cityname + "_keyword_search.txt"
	file_name = file_name.replace(' ', '')
	cf.validate_directory(out_file_path)
	output = open(out_file_path + file_name, 'w')

	output.write('keyword: ' + cityname + '\n')
	for p_id in place_id_dict:
		#print p + " ----> id:  " + place_dict[p] + "\n"
		s = p_id + ": " + place_id_dict[p_id][0] + ": " + place_id_dict[p_id][1]+ "\n"
		#decode s as UTF-8 string
		output.write(s.encode('utf-8'))
	output.close()

if __name__ == '__main__':
	main()
