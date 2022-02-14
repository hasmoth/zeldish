import pygame
from csv import reader
from os import walk
from tkinter import image_names

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

# dictionary = {
#   'style': import_csv_layout('path/to/file.csv')
# }

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for img in sorted(img_files):
            full_path = path + '/' + img
            img_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(img_surf)

    return surface_list


    # dictionary = {
    #   'style': import_folder('path/to/file')
    # }

