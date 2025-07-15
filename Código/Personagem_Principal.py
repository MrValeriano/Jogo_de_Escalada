from Definições import *

class Principal(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("Grafismos/Personagem_Principal/Idle/pixil-frame-0.png")
        self.rect = self.image.get_frect(center = pos)
        self.direction = vector()