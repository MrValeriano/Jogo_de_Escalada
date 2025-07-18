from Definições import *

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, pos, tipo, âncora, *groups):
        super().__init__(*groups)
        self.âncora = âncora
        self.frames = {
            "parado": {
                "direita": importar_pasta("Grafismos","Inimigos",tipo,"Idle","Direita"),
                "esquerda": importar_pasta("Grafismos","Inimigos",tipo,"Idle","Esquerda")
            },
            "andar": {
                "direita": importar_pasta("Grafismos","Inimigos",tipo,"Walk_Cycle","Direita"),
                "esquerda": importar_pasta("Grafismos","Inimigos",tipo,"Walk_Cycle","Esquerda")
            }
        }
        self.acção = "parado"
        self.lado = "direita"
        self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][self.indice_frame]
        self.rect = self.image.get_frect(center = pos)
        self.direção = vector()
    
    def movimentação(self, dt):
        #* escolha aleatória de acção dentro da plataforma de âncora
        self.acção = rd.sample(list(self.frames.keys()), 1)
        print(self.acção)
        self.rect.center += self.direção * 500 * dt

    def animação(self, dt):
        self.indice_frame += ANIMATION_SPEED * dt
        if int(self.indice_frame) >= len(self.frames[self.acção][self.lado]):
            self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][int(self.indice_frame)]

    def update(self, dt):
        self.movimentação(dt)
        self.animação(dt)
