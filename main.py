import os
import sys
import pygame
import requests
from functions import get_ll_spn, get_coordinates, get_nearest_object, geocode

toponym_to_find = "Красноярск, ул. Ленина, 114"
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": get_ll_spn(toponym_to_find)[0],
    "spn": get_ll_spn(toponym_to_find)[1],
    "l": "map"
}


def load_map(server, params, name):
    response = requests.get(server, params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(server + params)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = name
    with open(map_file, "wb") as file:
        file.write(response.content)


pygame.init()
screen = pygame.display.set_mode((600, 450))
width, height = screen.get_width(), screen.get_height()
load_map(map_api_server, map_params, "map1.png")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os.remove('map1.png')
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            mx, my = width - x, height - y
            coords = map_params['ll'][0], map_params['ll'][1]
            koefx, koefy = mx / float(coords[0]), my / float(coords[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                map_params = {
                    "ll": get_ll_spn(toponym_to_find)[0],
                    "spn": get_ll_spn(toponym_to_find)[1],
                    "l": "sat"
                }
                load_map(map_api_server, map_params, "map1.png")
            elif event.key == pygame.K_1:
                map_params = {
                    "ll": get_ll_spn(toponym_to_find)[0],
                    "spn": get_ll_spn(toponym_to_find)[1],
                    "l": "map"
                }
                load_map(map_api_server, map_params, "map1.png") 
            if event.key == pygame.K_2:
                map_params = {
                    "ll": get_ll_spn(toponym_to_find)[0],
                    "spn": get_ll_spn(toponym_to_find)[1],
                    "l": "sat,trf,skl"
                }
                load_map(map_api_server, map_params, "map1.png")            
                
    screen.blit(pygame.image.load('map1.png'), (0, 0))
    pygame.display.flip()
