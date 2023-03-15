from gps import *

near_coffee_shop_location = "106台北市大安區永康街37巷28號"
near_coffee_shop_dic = get_nearest_coffee_shop(near_coffee_shop_location)
lat = near_coffee_shop_dic['lat']
lng = near_coffee_shop_dic['lng']

# set
radius = 100
keyword = 'coffee'
nearby_coffee = get_nearby_places(lat, lng, radius, keyword)

if nearby_coffee:
    nearest_coffee_shop = nearby_coffee[0]
    photo_ref = nearest_coffee_shop['photos'][0]['photo_reference']
    photo_width = nearest_coffee_shop['photos'][0]['width']
    thumbnail_image_url = f"https://maps.googleapis.com/maps/api/place/photo?key={GOOGLE_API_KEY}&photoreference={photo_ref}&maxwidth={photo_width}"
    nearest_coffee_details = get_place_details(nearest_coffee_shop['place_id'])
    coffee_name = nearest_coffee_details['name']
    coffee_rating = nearest_coffee_details['rating']
    maps_url = f'https://www.google.com/maps/search/?api=1&query={lat},{lng}&query_place_id={nearest_coffee_shop["place_id"]}'
    print(f'Name: {coffee_name}')
    print(f'Rating: {coffee_rating}')
    print(f'Google Maps URL: {maps_url}')
    print(f'Coffee_shop_image_URL: {thumbnail_image_url}')
else:
    print('No nearby places found.')
