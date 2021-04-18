from citipy import citipy
import numpy as np

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