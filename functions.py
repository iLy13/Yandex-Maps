import requests
import math


def geocode(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}
    response = requests.get(geocoder_request, params=geocoder_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {response.status_code} ({response.reason})""")

    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return None, None
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_ll_spn(address):
    toponym = geocode(address)
    if not toponym:
        return None, None
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    envelope = toponym['boundedBy']['Envelope']
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx = abs(float(l) - float(r)) / 2
    dy = abs(float(t) - float(b)) / 2
    span = f"{dx},{dy}"
    return ll, span


def screen_to_geo(pos, ll, address):
    zoom = geocode(address)['zoom']
    coord_to_geo_x = 0.0000428
    coord_to_geo_y = 0.0000428
    dx = pos[0] - 300
    dy = 225 - pos[1]
    lx = float(ll.split(',')[0]) + dx * coord_to_geo_x * \
         math.cos(math.radians(float(ll.split(',')[1]))) * math.pow(2, 15 - int(zoom))
    ly = float(ll.split(',')[1]) + dy * coord_to_geo_y * \
         math.cos(math.radians(float(ll.split(',')[0]))) * math.pow(2, 15 - int(zoom))
    return lx, ly


def get_nearest_object(point, kind):
    ll = "{0},{1}".format(point[0], point[1])
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": '40d1649f-0493-4b70-98ba-98533de7710b',
        "geocode": ll,
        "format": "json"}
    if kind:
        geocoder_params['kind'] = kind
    response = requests.get(geocoder_request, params=geocoder_params)
    if not response:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {response.status_code,} ({response.reason})""")
    json_response = response.json()
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"]["name"] if features else None
