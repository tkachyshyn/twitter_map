import urllib.request, urllib.parse, urllib.error
import json
import oauth
import hidden
from geopy.geocoders import Nominatim
import folium

def increase(url, parameters):
    credentials = hidden.oauth()
    consumer = oauth.OAuthConsumer(credentials['consumer_key'],
                                     credentials['consumer_secret'])
    token = oauth.OAuthToken(credentials['token_key'], credentials['token_secret'])

    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                      token=token, http_method='GET', http_url=url,
                      parameters=parameters)
    oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(),
                                 consumer, token)
    return oauth_request.to_url()

def get_data(account:str):
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    url = increase(TWITTER_URL,
                        {'screen_name': account, 'count': '75'})

    Connection = urllib.request.urlopen(url)

    data = Connection.read().decode()

    js = json.loads(data)

    dictionary = dict()

    for i in range(len(js['users'])):
        user = js['users'][i]['screen_name']
        location = js['users'][i]['location']

        dictionary[user] = location

    return dictionary

def get_location(account:str):
    dictionary = get_data(account)

    for user in list(dictionary):
        location_set = []
        geolocator = Nominatim(user_agent='map')
        location = geolocator.geocode(user)

        if location != None:
            location_set.append(location.latitude)
            location_set.append(location.longitude)
            dictionary[user] = tuple(location_set)

        else:
            try:
                dictionary.pop(user)
                continue

            except Exception:
                continue
    return dictionary


def create_map(account:str):
    dictionary = get_location(account)

    key_lst = []
    coord_lst = []
    
    map = folium.Map()

    fg = folium.FeatureGroup(name = "pointers")
    for key in dictionary:
        username = key
        coords = dictionary[key]

        fg.add_child(folium.Marker(location = list(coords), popup = username, icon = folium.Icon()))

    map.add_child(fg)
    map.add_child(folium.LayerControl())

    map.save('templates/twitter_map.html')

# create_map()