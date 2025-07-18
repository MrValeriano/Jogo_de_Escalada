from Definições import *
from Processamento_do_input_do_jogador import input_jogador

class Principal(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("Grafismos/Personagem_Principal/Idle/pixil-frame-0.png")
        self.rect = self.image.get_frect(center = pos)
        self.dire = vector()
        self.facing = "right"
        self.frame
    
    def movimentação(self, dt):
        self.rect.center += self.direction * 500 * dt
    
    def update(self, dt):
        self.direction = input_jogador()
        self.movimentação(dt)