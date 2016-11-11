import twitter
import json
import sys
from credentials import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET
import os
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
	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)

	twitter_api = twitter.Twitter(auth=auth)
	argvs = sys.argv
	searched_country = ''
	if len(argvs) > 1:
		cityname = argvs[1]
		if argvs[2]:
			non_city_name = True
			print 'non_city_nam is True'
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
	if os.path.isdir(out_file_path) == False:
		print 'city name is wrong'
		quit()
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
