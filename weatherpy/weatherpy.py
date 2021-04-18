from citipy import citipy
import numpy as np
import requests
import time
from pprint import pprint

# get API key for Open Weather
from config.config import weather_api_key

output_folder = '../output_data/'
_output_data_file = output_folder.join('cities.csv')

lat_range = (-90, 90)
lng_range = (-180, 180)


def get_random_lat_lng():
    # generates a random set of latitude and longitude using numpy
    lats = np.random.uniform(lat_range[0], lat_range[1], size=1500)
    lngs = np.random.uniform(lng_range[0], lat_range[1], size=1500)
    coordinates = zip(lats, lngs)

    return coordinates


def get_nearest_city(coordinate):
    # takes a coordinate pair and uses citipy to return the name of the nearest city
    lat = coordinate[0]
    lng = coordinate[1]

    city = citipy.nearest_city(lat, lng).city_name

    return city


def generate_city_list():
    cities_list = []

    while len(cities_list) < 500:
        coordinate_list = get_random_lat_lng()

        for coordinate in coordinate_list:
            city = get_nearest_city(coordinate)

            if city not in cities_list:
                cities_list.append(city)

        if len(cities_list) < 500:
            print('city_list does not contain enough data. Running again')

    return cities_list


def get_weather_data(city_list):
    open_weather_url = 'http://api.openweathermap.org/data/2.5/weather?'
    param_dict = {
        'appid': weather_api_key,
        'units': 'imperial'
    }

    weather_data = []
    i = 1

    def query_open_weather_api(city):
        param_dict['q'] = city
        response = requests.get(open_weather_url, param_dict).json()

        coord_info = response['coord']
        temp_info = response['main']
        cloudiness = response['clouds']['all']
        wind_speed = response['wind']['speed']
        country = response['sys']['country']
        date = response['dt']

        weather_dict = {
            'City': city,
            'Lat': coord_info['lat'],
            'Lng': coord_info['lon'],
            'Max Temp': temp_info['temp_max'],
            'Humidity': temp_info['humidity'],
            'Cloudiness': cloudiness,
            'Wind Speed': wind_speed,
            'Country': country,
            'Date': date
        }

        return weather_dict

    for city in city_list:
        city_weather = query_open_weather_api(city)
        weather_data.append(city_weather)
        print(i)
        i+=1


    print(weather_data)


city_list = generate_city_list()
get_weather_data(city_list)