from gps import *
import os
import requests
from linebot.models import TextSendMessage, LocationSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn

# function to get the address from the LocationMessage event
def get_address(event):
    latitude = event.message.latitude
    longitude = event.message.longitude
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_API_KEY}"
    response = requests.get(url).json()
    if response['status'] == 'OK':
        return response['results'][0]['formatted_address']
    else:
        return None


def algorithm(location, coffee):
    i = 0
    distance_list = []
#     distance_dic = {}
    while True:
        if i == len(coffee):
            break
#         temp_name = get_place_details(coffee[i]['place_id'])['name']
        cf_lat, cf_lng = coffee[i]['geometry']['location']['lat'], coffee[i]['geometry']['location']['lng']
        user_lat, user_lng = users_loc(location)['lat'], users_loc(location)['lng']
        temp_distance = haversine(user_lat, user_lng, cf_lat, cf_lng)
        distance_list.append(temp_distance)
#         distance_dic[temp_name] = temp_distance
        i += 1
    nearest_cf_index = distance_list.index(min(distance_list))
#     print(distance_dic)
    return nearest_cf_index

def nearest_coffee(location):
    near_coffee_shop_dic = users_loc(location)
    lat = near_coffee_shop_dic['lat']
    lng = near_coffee_shop_dic['lng']
    
    # settings
    radius = 500
    keyword = 'coffee'
    nearby_coffee = get_nearby_places(lat, lng, radius, keyword)


    if nearby_coffee:
        nearest_coffee_shop = nearby_coffee[algorithm(location, nearby_coffee)]
        photo_ref = nearest_coffee_shop['photos'][0]['photo_reference']
        photo_width = nearest_coffee_shop['photos'][0]['width']
        thumbnail_image_url = f"https://maps.googleapis.com/maps/api/place/photo?key={GOOGLE_API_KEY}&photoreference={photo_ref}&maxwidth={photo_width}"
        nearest_coffee_details = get_place_details(nearest_coffee_shop['place_id'])
        coffee_name = nearest_coffee_details['name']
        coffee_rating = nearest_coffee_details['rating']
        maps_url = f'https://www.google.com/maps/search/?api=1&query={lat},{lng}&query_place_id={nearest_coffee_shop["place_id"]}'
        # print(f'Name: {coffee_name}')
        # print(f'Rating: {coffee_rating}')
        # print(f'Google Maps URL: {maps_url}')
        # print(f'Coffee_shop_image_URL: {thumbnail_image_url}')
        return [coffee_name, coffee_rating, maps_url, thumbnail_image_url]
    else:
        # print('No nearby places found.')
        return 0
