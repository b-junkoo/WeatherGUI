# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 11:03:15 2021
Connects to Weather.gov's api and retrieves week's forecast
@author: jko
"""

import requests
from geopy.geocoders import Nominatim
import json

def coord():
    while True:
        try:
            Address = u_input()
            geolocator = Nominatim(user_agent = 'Weather_Scraper')
            location = geolocator.geocode(Address)
            lat = location.latitude
            long = location.longitude
            break
        except AttributeError:
            print('Please enter a valid input')
    return (lat, long)
        
def u_input():
    user_input = input("Enter an Address, City, or Zip Code: ")
    return user_input

def grid():
    coor = coord()
    grid = requests.get('https://api.weather.gov/points/{lat},{long}'.format(
            lat=coor[0],long=coor[1]))
    grid = grid.content
    return json.loads(grid)

def forecast():
    while True:
        try:
            grids = grid()
            forecasts = requests.get(grids['properties']['forecast'])
            forecasts = forecasts.content
            break
        except KeyError:
            print('Try again')
    return [json.loads(forecasts)['properties']['periods'],grids['properties']['relativeLocation']['properties']]

if __name__ == "__main__":
    a = forecast()
    
   