import twitter
import json
import sys
from credentials import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET
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
	print "parameter for geo search"
	#print "query (city name etc)= ",
	cityname = raw_input('query (city name etc)=' )
	#print "granularity (poi, neighborhood, city, admin, country) = ",
	granularity = raw_input("granularity (poi, neighborhood, city, admin, country) = ")
	latitude = raw_input('latitude = ')
	longtitude = raw_input('longtitude = ')
	argvs = sys.argv
	searched_country = ''
	if len(argvs) == 2:
		searched_country = argvs[1]
	
	accuracy = 10000
	if latitude and longtitude and cityname and granularity:
		result = twitter_api.geo.search(query=cityname, granularity=granularity, lat=latitude, long=longtitude, accuracy=accuracy)
	elif latitude and longtitude and cityname:
		result = twitter_api.geo.search(query=cityname, lat=latitude, long=longtitude)
	elif latitude and longtitude:
		result = twitter_api.geo.search(lat=latitude, long=longtitude)
	elif cityname and granularity:
		result = twitter_api.geo.search(query=cityname, granularity=granularity)
	elif cityname:
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
		
	if latitude and longtitude:
		area_range = accuracy / 1000 #km
		file_name = "placeid_" + latitude + "_" + longtitude + "_" + str(area_range) + "km_"+ ".txt"
	else:
		if granularity:
			file_name = "placeid_" + cityname + "_" + granularity + ".txt"
		else:
			file_name = "placeid_" + cityname + ".txt"
	file_name = file_name.replace(' ', '')
	out_file_path = "/home/muga/twitter/place_id_data/"
	output = open(out_file_path + file_name, 'w')

	output.write('city name: ' + cityname + ', granularity: ' + granularity + ', latitude: ' + latitude + ', longtitude: ' + longtitude + "\n")
	for p_id in place_id_dict:
		#print p + " ----> id:  " + place_dict[p] + "\n"
		s = p_id + ": " + place_id_dict[p_id][0] + ": " + place_id_dict[p_id][1]+ "\n"
		#decode s as UTF-8 string
		output.write(s.encode('utf-8'))
	output.close()

if __name__ == '__main__':
	main()
