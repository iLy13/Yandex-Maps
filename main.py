import os
import sys
import pygame
import requests
from yandex_functions import get_ll_spn, get_coordinates, get_nearest_object, geocode

toponym_to_find = "Красноярск, ул. Ленина, 114"


def load_map(resp, name):
    response = requests.get(resp)
    if not response:
        print("Ошибка выполнения запроса:")
        print(resp)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = name
    with open(map_file, "wb") as file:
        file.write(response.content)


map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": get_ll_spn(toponym_to_find)[0],
    "spn": get_ll_spn(toponym_to_find)[1],
    "l": "map"
}

pygame.init()
screen = pygame.display.set_mode((600, 450))
response = requests.get(map_api_server, params=map_params)
load_map(toponym_to_find, "map.png")

running = True
while running:
    screen.blit(pygame.image.load(map), (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os.remove(map)
    screen.blit(pygame.image.load(map), (0, 0))
    pygame.display.flip()
