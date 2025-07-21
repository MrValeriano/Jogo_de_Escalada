import pygame
from pytmx.util_pygame import load_pygame
from os.path import join
from os import walk
from pygame.math import Vector2 as vector
import random as rd

def importar_pasta(*path):
    frames = []
    for pasta, subpasta, imagens in walk(join(*path)):
        for nome in sorted(imagens, key = lambda name: int(name.split(".")[0])):
            fullpath = join(pasta, nome)
            surf = pygame.image.load(fullpath).convert_alpha()
            frames.append(surf)
    return frames

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
TILE_SIZE = 96
ANIMATION_SPEED = 20
HANDMADE_LEVELS = ["25", "50", "75", "100"]
EMPTY_EDGES = [12, 12]
pygame.display.set_caption('Jogo de Escalada')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()