import twitter
import json
import sys
import os
from credentials import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET
import time
import common_functions as cf
def getCoordinates(city_name, keyword):
	data_path = '/home/muga/twitter/place_id_data/' + city_name + '/'
	file_name = ''
	#print 'city name: ' + city_name
	for f in os.listdir(data_path):
		if city_name in f and f.endswith('txt') and f.startswith('coordinate') and keyword in f:
			file_name = data_path + f
			break
	if len(file_name) == 0:
		print 'The Input File is not Found. Abort'
		quit()

	input = open(file_name, 'r')
	s = input.readline()

	coodinate_dict = {}
	while s: #until the end of the file
		splitted_line =  s.split(',')
		if not len(splitted_line) == 3:
			s = input.readline()
		place_name = splitted_line[0]
		latitude = splitted_line[1]
		longtitude = splitted_line[2]
		coordinate = [latitude, longtitude]
		coodinate_dict[place_name] = coordinate
		s = input.readline()
	return coodinate_dict

def geo_search(twitter_api, place_name, latitude, longtitude):
	if not latitude or not longtitude:
		print 'latitude: ' + latitude + ', longtitude ' + longtitude
		quit()

	print 'place name: %s, latitude:%.2f, longtitude:%.2f' % (place_name, latitude, longtitude)
	accuracy = 10000
	result = twitter_api.geo.search(lat=latitude, long=longtitude,accuracy=accuracy)
	places_info = result['result']['places']
	return places_info

def write_place_info(places_info, place_name, output):
	place_id_dict = {}
	for place in places_info:#
		place_full_name = place['full_name']
		place_name = place['name']
		place_id = place['id']
		country = place['country']
		place_list = [place_full_name, place_name]
		place_id_dict[place_id] = place_list
		
	for p_id in place_id_dict:
		#print p + " ----> id:  " + place_dict[p] + "\n"
		s = p_id + ": " + place_id_dict[p_id][0] + ": " + place_id_dict[p_id][1]+ "\n"
		#decode s as UTF-8 string
		output.write(s.encode('utf-8'))
	
	return


def main():
	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)

	twitter_api = twitter.Twitter(auth=auth)
	if len(sys.argv) > 1:
		cityname = sys.argv[1]
		if len(sys.argv) == 3:
			wait_time = int(sys.argv[2])
			print 'Please wait for ' + sys.argv[2] + ' minutes'
			time.sleep(60*wait_time + 5)

	else:
		cityname = raw_input('query (London, NewYork etc)=' )
	#print "granularity (poi, neighborhood, city, admin, country) = ",
	if len(sys.argv) < 2 and cityname == 'London':
		print 'Please Input Keyword. e.g. centre, outer'
		quit()
	if cityname == 'London':
		keyword = sys.argv[1]
	else:
		keyword = ''

	coodinate_dict = getCoordinates(cityname, keyword)
	count_invoke = 0
	out_file_path = "/home/muga/twitter/place_id_data/" + cityname + '/'
	cf.validate_directory(out_file_path)
	if keyword:
		file_name = "placeid_" + keyword + "_" + cityname + "_coordinate_search.txt"
	else:
		file_name = "placeid_" + cityname + "_coordinate_search.txt"
	output = open(out_file_path + file_name, 'w')

	for place_name in coodinate_dict.keys():
		coordinate = coodinate_dict[place_name] 
		latitude = float(coordinate[0])
		longtitude = float(coordinate[1])
		if count_invoke == 13:
			print 'Sleep for 15 minutes...zz....' 
			time.sleep(60*15 + 5)
			print '..zz...Awake !! Restart'
			count_invoke = 0
		places_info = geo_search(twitter_api, place_name, latitude, longtitude)
		count_invoke += 1
		output.write('place name: ' + place_name + ', latitude: ' + str(latitude) + ', longtitude: ' + str(longtitude) + "\n")
		write_place_info(places_info, place_name, output) 

	output.close()
if __name__ == '__main__':
	main()
