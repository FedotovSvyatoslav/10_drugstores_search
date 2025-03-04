import math
import os
import requests
from PIL import Image
import sys
from dotenv import load_dotenv

load_dotenv()

GEOCODER_API_KEY = os.getenv("GEOCODER_API_KEY",
                             "40d1649f-0493-4b70-98ba-98533de7710b")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY",
                           "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3")


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = map(float, a)
    b_lon, b_lat = map(float, b)
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    return math.sqrt(dx * dx + dy * dy)


def find_drugstores(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": GEOCODER_API_KEY,
        "geocode": address,
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print("Ошибка геокодирования")
        return

    json_response = response.json()
    toponym = \
        json_response["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"]
    address_point = toponym["Point"]["pos"].split()
    address_ll = ",".join(address_point)
    address_coords = address_point

    # Поиск аптек
    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": SEARCH_API_KEY,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz",
        "results": 10
    }
    org_response = requests.get(search_api_server, params=search_params)
    if not org_response:
        print("Ошибка поиска аптек")
        return

    org_json_response = org_response.json()
    drugstores = []
    pt = ""
    for organization in org_json_response["features"]:
        point = organization["geometry"]["coordinates"]
        org_name = organization["properties"]["name"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]
        distance = lonlat_distance(address_coords, point)
        org_hours = \
            organization["properties"]["CompanyMetaData"].get("Hours",
                                                              {}).get(
                "Availabilities", [{}])[0]

        color = "gr"
        if "Everyday" in org_hours:
            color = "gn"
        elif "Intervals" in org_hours:
            color = "bl"

        org_mark = f"{point[0]},{point[1]},pm2{color}l"
        pt = f"{pt}~{org_mark}" if pt else org_mark
        drugstores.append(
            {"name": org_name, "address": org_address, "distance": distance,
             "coords": point})

    # Сортировка по расстоянию
    drugstores.sort(key=lambda x: x["distance"])

    # Вывод информации
    print(f"Найдено {len(drugstores)} аптек рядом с '{address}':")
    for i, drugstore in enumerate(drugstores, 1):
        print(
            f"{i}. {drugstore['name']} ({drugstore['address']}) - {drugstore['distance']:.0f} м")

    # Создание карты
    map_params = {
        "ll": address_ll,
        "l": "map",
        "pt": pt
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    if response:
        with open("map.png", "wb") as f:
            f.write(response.content)
        Image.open("map.png").show()
    else:
        print("Ошибка загрузки карты")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python drugstores_map.py <адрес>")
        sys.exit(1)
    address = " ".join(sys.argv[1:])
    find_drugstores(address)
