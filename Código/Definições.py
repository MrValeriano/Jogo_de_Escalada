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
    def __init__(self, duração, repetir = False, autoiniciar = False, fun = None):
        self.duração = duração
        self.função = fun
        self.início = 0
        self.activo = False
        self.repetir = repetir
        if autoiniciar: self.activar()
        
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
    "Calças": ["Calças de armadura!", "Protegem dessas desgraçadas tartarugas!", "Custam 15$!"],
    "Apicultor": ["Um casaco de apicultor!", "Protege dessas malditas vespas!", "Custa 15$!"],
    "Sapato": ["As botas de Hermes!", "Permitem saltar uma segunda\nvez, no ar!", "Custa 25$!"],
    "Coração": ["Levou das boas, hein, comparsa?", "Compre para recuperar uma vida!", "Custa 50$!"],
    "Conversa": [["Ohoh! Boas, compadre!", "Como vai isso?"],
                 ["Aquela maldita bicharada lá fora...", "A fazer a vida negra a quem tenta escalar!",
                  "Ainda hei-de arranjar maneira\nde me livrar destas pestes!"]]
}

class DialogTree:
    def __init__(self, target, position, all_sprites, end_dialog, lastline = False, custom_single = None):
        self.target = target
        self.font = fonts["dialog"]
        self.all_sprites = all_sprites
        self.position = position
        self.end_dialog = end_dialog
        #* escolher mensagem
        if target == "Conversa":
            self.dialog = falas["Conversa"][rd.randrange(len(falas["Conversa"]))]
        else:
            self.dialog = falas[self.target] if not custom_single else custom_single
        self.dialog_num = len(self.dialog)
        self.dialog_index = 0 if not lastline else self.dialog_num-1
        
        self.cur_dialog = DialogSprite(self.dialog[self.dialog_index], position, self.font, self.all_sprites)
        self.dialog_buffer = Timer(500, autoiniciar=True)
        self.dialog_timer = Timer(2000)
        self.dialog_timer.activar()
    
    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE]:
            if not self.dialog_buffer.activo:
                self.cur_dialog.kill()
                self.dialog_index += 1
                if self.dialog_index < self.dialog_num:
                    self.cur_dialog = DialogSprite(self.dialog[self.dialog_index], self.position, self.font, self.all_sprites)
                    self.dialog_buffer.activar()
                    self.dialog_timer.activar()
                else:
                    self.end_dialog(self.target)
        else:
            if not self.dialog_timer.activo:
                self.cur_dialog.kill()
                self.dialog_index += 1
                if self.dialog_index < self.dialog_num:
                    self.cur_dialog = DialogSprite(self.dialog[self.dialog_index], self.position, self.font, self.all_sprites)
                    self.dialog_buffer.activar()
                    self.dialog_timer.activar()
                else:
                    self.end_dialog(self.target)
    
    def update(self):
        self.dialog_buffer.actualizar()
        self.dialog_timer.actualizar()
        self.input()

class DialogSprite(pygame.sprite.Sprite):
    def __init__(self, msg, pos, font, *groups):
        super().__init__(*groups)
        #* texto
        text_surf = font.render(msg, False, "black")
        padding = 15
        width = max(200, text_surf.get_width() + padding * 2)
        height = text_surf.get_height() + padding * 2
        #* fundo
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill((0,0,0,0))
        pygame.draw.rect(surf, "#ffffff", surf.get_frect(topleft = (0,0)), 0, 10)
        surf.blit(text_surf, text_surf.get_frect(center = (width/2, height/2)))
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos + vector(0, -10))
    
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