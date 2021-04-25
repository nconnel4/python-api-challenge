from citipy import citipy
import numpy as np
import requests

# get API key for Open Weather
from config.config import weather_api_key

output_folder = '../output_data/'
output_data_file = output_folder + 'cities.csv'

lat_range = (-90, 90)
lng_range = (-180, 180)


class Error(Exception):
    """Base class for exceptions"""
    pass


class InvalidCityError(Error):
    """Returned when Open Weather API returns a 404 error for city"""

    def __init__(self, city, message='City not found in Open Weather API'):
        self.city = city
        self.message = f'{city} not found by Open Weather API'
        super().__init__(self.message)


class TooManyAPICallsError(Error):
    """Returned if too many requests are made to the API within a minute"""
    pass


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

    while len(cities_list) < 550:
        coordinate_list = get_random_lat_lng()

        for coordinate in coordinate_list:
            city = get_nearest_city(coordinate)

            if city not in cities_list:
                cities_list.append(city)

        if len(cities_list) < 550:
            print('city_list does not contain enough data. Running again')

    return cities_list


def get_weather_data(city_list):
    weather_data = []

    def query_open_weather_api(city):
        open_weather_url = 'http://api.openweathermap.org/data/2.5/weather?'
        param_dict = {
            'appid': weather_api_key,
            'units': 'imperial',
            'q': city
        }

        response = requests.get(open_weather_url, param_dict)

        if response.status_code == 404:
            raise InvalidCityError(city)
        elif response.status_code == 429:
            raise TooManyAPICallsError()

        response_json = response.json()

        return response_json

    def process_response(response_json):
        coord_info = response_json['coord']
        temp_info = response_json['main']
        cloudiness = response_json['clouds']['all']
        wind_speed = response_json['wind']['speed']
        country = response_json['sys']['country']
        date = response_json['dt']

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

    # instantiate counter
    i = 0
    set = 0

    print('Data Retrieval Start')
    print('_________________________')

    for city in city_list:
        if i % 50 == 0:
            set += 1
            i = 0

        try:
            api_response = query_open_weather_api(city)
        except InvalidCityError:
            print('City not found. Skipping...')
            continue

        city_weather = process_response(api_response)

        # increment counter
        i+=1

        print(f'Processing Record {i} of Set {set} | {city}')
        weather_data.append(city_weather)

    print('_________________________')
    print('Data Retrieval End')

    return weather_data
