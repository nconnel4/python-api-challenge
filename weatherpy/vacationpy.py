import pandas as pd
import requests
from pprint import pprint

from config.config import google_api_key


class Error(Exception):
    """Base class for exceptions"""
    pass


class ZeroResultsError(Error):
    """Returned when Google Places doesn't return data"""
    pass


def get_hotels(cities_df: pd.DataFrame):

    hotel_list = []

    def query_google_places(latitude, longitude):
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

        params = {
            'location': f'{latitude}, {longitude}',
            'type': 'lodging',
            'key': google_api_key,
            'radius': 5000,
            'keyword': 'hotel'
        }

        with requests.get(url, params) as response:
            if response.status_code == 200:
                response_json = response.json()

            if response_json['status'] == 'ZERO_RESULTS':
                raise ZeroResultsError

        return response_json

    for index, row in cities_df.iterrows():
        lat = row['Lat']
        lng = row['Lng']

        # skip city if no results returned
        try:
            hotels = query_google_places(lat, lng)
        except ZeroResultsError:
            continue

        first_hotel = hotels['results'][0]
        lat = first_hotel['geometry']['location']['lat']
        lng = first_hotel['geometry']['location']['lng']

        hotel_info = {
            'hotel_name': first_hotel['name'],
            'marker': [lat, lng]
         }

        hotel_info['info_box'] = f'''
        <dl>
        <dt>Hotel Name</dt><dd>{hotel_info["hotel_name"]}</dd>
        <dt>City</dt><dd>{row["City"]}</dd>
        <dt>Country</dt><dd>{row["Country"]}</dd>
        </dl>
        '''

        hotel_list.append(hotel_info)

    return hotel_list

