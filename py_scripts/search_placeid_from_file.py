import twitter
import json
import sys
import os
from credentials import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET

def getPlaceID(city_name):
	data_path = '/home/muga/twitter/place_id_data/' + city_name + '/'
	file_name = ''
	#print 'city name: ' + city_name
	for f in os.listdir(data_path):
		if city_name in f and f.endswith('txt') and 'coordinate' in f:
			file_name = data_path + f
			#print 'file_name: ' + file_name
			break
	if len(file_name) == 0:
		print 'The Input File is not Found. Abort'
		quit()

	input = open(file_name, 'r')
	s = input.readline()

	place_info_dict = {}
	while s: #until the end of the file
		splitted_line =  s.split(',')
		place_name = splitted_line[0]
		latitude = splitted_line[1]
		longtitude = splitted_line[2]
		coordinate = [latitude, longtitude]
		place_info_dict[place_name] = coordinate
		s = input.readline()
	return place_info_dict

def geo_search(twitter_api, place_name, latitude, longtitude):
	if not latitude or not longtitude:
		print 'latitude: ' + latitude + ', longtitude ' + longtitude
		quit()

	print 'place name: %s, latitude:%.2f, longtitude:%.2f' % (place_name, latitude, longtitude)
	result = twitter_api.geo.search(lat=latitude, long=longtitude)
	places = result['result']['places']
	return places

def write_place_info(place_ids, place_name,  latitude, longtitude, cityname):
	accuracy = 10000
	place_id_dict = {}
	for place in place_ids:
		place_full_name = place['full_name']
		place_name = place['name']
		place_id = place['id']
		country = place['country']
		place_list = [place_full_name, place_name]
		place_id_dict[place_id] = place_list
		
	if latitude and longtitude:
		area_range = accuracy / 1000 #km
		file_name = "placeid_" + place_name + "_" + str(area_range) + "km_"+ ".txt"
	else:
		print 'abort'
		quit()
	file_name = file_name.replace(' ', '')
	out_file_path = "/home/muga/twitter/place_id_data/" + cityname + '/'
	output = open(out_file_path + file_name, 'w')
	output.write('city name: ' + place_name + ', latitude: ' + str(latitude) + ', longtitude: ' + str(longtitude) + "\n")
	for p_id in place_id_dict:
		#print p + " ----> id:  " + place_dict[p] + "\n"
		s = p_id + ": " + place_id_dict[p_id][0] + ": " + place_id_dict[p_id][1]+ "\n"
		#decode s as UTF-8 string
		output.write(s.encode('utf-8'))
	output.close()
	
	return


def main():
	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)

	twitter_api = twitter.Twitter(auth=auth)
	cityname = raw_input('query (London, NewYork etc)=' )
	#print "granularity (poi, neighborhood, city, admin, country) = ",
	argvs = sys.argv

	place_info_dict = getPlaceID(cityname)


	for place_name in place_info_dict.keys():
		coordinate = place_info_dict[place_name] 
		latitude = float(coordinate[0])
		longtitude = float(coordinate[1])
		places = geo_search(twitter_api, place_name, latitude, longtitude)
		write_place_info(places, place_name, latitude, longtitude, cityname) 

if __name__ == '__main__':
	main()
