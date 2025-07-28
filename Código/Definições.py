import pygame
from pytmx.util_pygame import load_pygame
from os.path import join
from os import walk
from pygame.math import Vector2 as vector
import random as rd

# Funções e classes auxiliares
def importar_pasta(*path):
    frames = []
    for pasta, subpasta, imagens in walk(join(*path)):
        for nome in sorted(imagens, key = lambda name: int(name.split(".")[0])):
            fullpath = join(pasta, nome)
            surf = pygame.image.load(fullpath).convert_alpha()
            frames.append(surf)
    return frames

class Timer:
    def __init__(self, duração, fun = None, repetir = False):
        self.duração = duração
        self.função = fun
        self.início = 0
        self.activo = False
        self.repetir = repetir
        
    def activar(self):
        self.activo = True
        self.início = pygame.time.get_ticks()
    
    def desactivar(self):
        self.activo = False
        self.início = 0
        if self.repetir:
            self.activar()
    
    def actualizar(self):
        tempo_actual = pygame.time.get_ticks()
        if tempo_actual - self.início >= self.duração:
            if self.função and self.início != 0:
                self.função()
            self.desactivar()

falas = {
    "Calças": "Protegem de tartarugas",
    "Apicultor": "Protege de abelhas",
    "Chicote": "Remover!",
    "Coração": "Vida extra!",
    "Conversa": "Como vai isso?"
}

class DialogTree:
    def __init__(self, item, player, all_sprites, font):
        self.player = player
        self.item = item
        self.font = font
        self.all_sprites = all_sprites
        
        self.dialog = item.get_dialog()
        self.dialog_num = len(self.dialog)
        self.dialog_index = 0
        
        self.cur_dialog = DialogSprite(self.dialog[self.dialog_index], self.item, self.font, self.all_sprites)

class DialogSprite(pygame.sprite.Sprite):
    def __init__(self, msg, pos, font, *groups):
        super().__init__(*groups)
        text_surf = font.render(msg, False, "black")
        self.image = text_surf
        self.rect = self.image.get_frect(bottomright = pos.rect.midtop + vector(0, -10))
    
# Constantes
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
TILE_SIZE = 96
ANIMATION_SPEED = 10
HANDMADE_LEVELS = ["25", "50", "75", "100"]
EMPTY_EDGES = [12, 12]

DEBUGGING = False

# Activação do package pygame
pygame.init()

pygame.display.set_caption('Jogo de Escalada')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
fonts = {
    "dialog": pygame.font.Font(join("Grafismos", "minecraftia", "Minecraftia-Regular.ttf"), 30),
    "HUD": pygame.font.Font(join("Grafismos", "minecraftia", "Minecraftia-Regular.ttf"), 50)
}