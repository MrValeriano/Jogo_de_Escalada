from Definições import *

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, tipo, âncora, *groups):
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
        self.pos = (self.âncora.rect.midtop[0], self.âncora.rect.midtop[1] - (self.image.height / 2))
        self.rect = self.image.get_frect(center = self.pos)
        self.direção = vector()
    
    def actividade(self, dt):
        #* esperar o fim da acção anterior
        if int(self.indice_frame) == 0:
            #* escolha aleatória de acção dentro da plataforma de âncora
            self.acção = rd.sample(list(self.frames.keys()), 1)[0]
            if self.rect.right >= self.âncora.rect.right:
                self.lado = "esquerda"
            elif self.rect.left <= self.âncora.rect.left:
                self.lado = "direita"
        if self.acção == "andar":
            if self.lado == "direita" and not self.rect.right >= self.âncora.rect.right:
                self.direção.x += 1
            elif self.lado == "esquerda" and not self.rect.left <= self.âncora.rect.left:
                self.direção.x -= 1
        else:
            self.direção = vector()
        self.rect.center += self.direção * 50 * dt

    def animação(self, dt):
        self.indice_frame += ANIMATION_SPEED * dt
        if int(self.indice_frame) >= len(self.frames[self.acção][self.lado]):
            self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][int(self.indice_frame)]

    def update(self, dt):
        self.actividade(dt)
        self.animação(dt)
