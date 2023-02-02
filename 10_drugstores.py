import math

import requests
from io import BytesIO
from PIL import Image
import sys


def get_object_scale(lower_corner, upper_corner):
    leftdown_angle = tuple(map(float, lower_corner.split()))
    rightup_angle = tuple(map(float, upper_corner.split()))
    width_degrees = abs(rightup_angle[0] - leftdown_angle[0])
    height_degrees = abs(rightup_angle[1] - leftdown_angle[1])
    return f"{width_degrees},{height_degrees}"


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance


toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if response:
    address_json_response = response.json()
    toponym = address_json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    address_point = toponym["Point"]["pos"].split(" ")
    address_longitude, address_lattitude = address_point
    address_ll = ",".join([address_longitude, address_lattitude])

    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz",
        "results": 10
    }
    search_api_server = "https://search-maps.yandex.ru/v1/"
    org_response = requests.get(search_api_server, params=search_params)
    org_json_response = org_response.json()

    pt = ""
    for organization in org_json_response["features"]:
        point = organization["geometry"]["coordinates"]
        org_point = f"{point[0]},{point[1]}"
        org_hours = organization["properties"]["CompanyMetaData"]["Hours"][
            "Availabilities"][0]
        if "Everyday" in org_hours:
            color = "gn"
        elif "Intervals" in org_hours:
            color = "bl"
        else:
            color = "gr"
        org_mark = f"{org_point},pm2{color}l"
        if pt:
            pt = pt + '~' + org_mark
        else:
            pt = org_mark

    map_params = {
        "ll": address_ll,
        "l": "map",
        "pt": pt
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(response.content)).show()
