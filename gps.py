# # To get the nearest coffee shop depending on where the user is at the moment.
# # Google GPS (Global Position System)
# # Algorithm -> get 3 coffee shops in total and then compare each score, get the highest one, aka most recommended coffee shop.
# # Turn all coffee shops' IP(interner protocol協議) address into longitude and latitude. Thus, save the data into a csv file.

# import os
# import requests

# os.environ['GOOGLE_API_KEY'] = "AIzaSyA2ReggIbRz5s1zFCDyxXcnwXRWHucFJug"
# # Define the function that retrieves the nearest coffee shop
# def get_nearest_coffee_shop(location):
#     # Use the Google Geocoding API to convert the location into coordinates
#     geocoding_url = url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={os.environ["GOOGLE_API_KEY"]}'
#     geocoding_response = requests.get(geocoding_url).json()
#     latitude = geocoding_response['results'][0]['geometry']['location']['lat']
#     longitude = geocoding_response['results'][0]['geometry']['location']['lng']
#     # print("Latituded:", latitude, "Longitude:", longitude) Our location

#     # Use the Google Places API to search for nearby coffee shops
#     places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=100&type=cafe&key={os.environ['GOOGLE_API_KEY']}"
#     # places_url -> all coffee shops that within radius 500 (HTML)
#     places_response = requests.get(places_url).json()
#     # places_response -> dictionary with diff. attributes

#     # Find the nearest coffee shop
#     nearest_shop = places_response['results'][0]
#     name = nearest_shop['name']
#     address = nearest_shop['vicinity']
#     rating = nearest_shop.get('rating', 'N/A')
#     lat = nearest_shop["geometry"]["location"]["lat"]
#     lng = nearest_shop["geometry"]["location"]["lng"]

#     # Return the coffee shop details
#     return {"name": name, "address": address, "rating": rating, "lat": lat, "long":lng}

# # the function will return me a dictionary with different elemensts of the coffee shop
# near_coffee_shop_location = "106台北市大安區永康街37巷28號"
# near_coffee_shop_dic = get_nearest_coffee_shop(near_coffee_shop_location)
# print(f"{near_coffee_shop_dic['name'], near_coffee_shop_dic['rating'], near_coffee_shop_dic['address']}") 

# # near_coffee_shop is a dictionary
# nearest_coffee_name = near_coffee_shop_dic["name"]
# nearest_coffee_address = near_coffee_shop_dic["address"]
# nearest_coffee_rating = near_coffee_shop_dic["rating"]
# nearest_coffee_lat = near_coffee_shop_dic["lat"]
# nearest_coffee_lng = near_coffee_shop_dic["long"]

# # the Google Maps URL
# nearest_coffee_GoogleMaps = f'https://www.google.com/maps/search/?api=1&query={nearest_coffee_lat},{nearest_coffee_lng}'
# print(nearest_coffee_GoogleMaps)

import requests
from math import radians, cos, sin, asin, sqrt

GOOGLE_API_KEY = "AIzaSyA2ReggIbRz5s1zFCDyxXcnwXRWHucFJug"

# calculate the "nearest" coffee shop!
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def users_loc(location):
    # Use the Google Geocoding API to convert the location into coordinates
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_API_KEY}'
    geocoding_response = requests.get(geocoding_url).json()
    lat = geocoding_response['results'][0]['geometry']['location']['lat']
    lng = geocoding_response['results'][0]['geometry']['location']['lng']
    # lat & lng here will be the user's current location
    return {'lat': lat, 'lng': lng}

def get_nearby_places(lat, lng, radius, keyword):
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&keyword={keyword}&key={GOOGLE_API_KEY}'
    response = requests.get(url).json()
    return response['results']

def get_place_details(place_id):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}'
    response = requests.get(url).json()
    return response['result']
