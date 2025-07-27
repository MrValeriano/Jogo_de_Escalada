from Definições import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.frames = {
            "parado": {
                "direita": importar_pasta("Grafismos","Vendedor","Idle","Direita"),
                "esquerda": importar_pasta("Grafismos","Vendedor","Idle","Esquerda")
            },
            "falar": {
                "direita": importar_pasta("Grafismos","Vendedor","Talking","Direita"),
                "esquerda": importar_pasta("Grafismos","Vendedor","Talking","Esquerda")
            }
        }
        self.acção = "parado"
        self.lado = "esquerda"
        self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][self.indice_frame]
        self.rect = self.image.get_frect(center = pos)
    
    def animação(self, dt):
        jogador = self.groups()[0].sprites()[-1]
        if jogador.rect.centerx > self.rect.centerx:
            self.lado = "direita"
        else:
            self.lado = "esquerda"
        self.indice_frame += (ANIMATION_SPEED / 2) * dt
        if int(self.indice_frame) >= len(self.frames[self.acção][self.lado]):
            self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][int(self.indice_frame)]

    def update(self, dt):
        self.animação(dt)