import os
import sys
import pygame
import requests
from functions import get_ll_spn, get_coordinates, get_nearest_object, geocode

toponym_to_find = "Красноярск, ул. Ленина, 114"
map_api_server = "http://static-maps.yandex.ru/1.x/"
point = "{0},{1}".format(get_coordinates(toponym_to_find)[0], get_coordinates(toponym_to_find)[1])
map_params = {
    "ll": get_ll_spn(toponym_to_find)[0],
    "spn": get_ll_spn(toponym_to_find)[1],
    "l": "map"
    "pt": "{0},pm2dgl".format(point)
}
map1 = 'http://static-maps.yandex.ru/1.x/?ll=92.854072,56.012447&l=map&z=18'


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


pygame.init()
screen = pygame.display.set_mode((600, 450))
load_map(map1, "map1.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os.remove('map1.png')
    screen.blit(pygame.image.load('map1.png'), (0, 0))
    pygame.display.flip()
