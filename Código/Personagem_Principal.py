from Definições import *
from Processamento_do_input_do_jogador import input_jogador

class Principal(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.frames = {
            "parado": {
                "direita": importar_pasta("..","Grafismos","Personagem_Principal","Idle","Direita"),
                "esquerda": importar_pasta("..","Grafismos","Personagem_Principal","Idle","Esquerda")
            },
            "andar": {
                "direita": importar_pasta("..","Grafismos","Personagem_Principal","Walk_Cycle","Direita"),
                "esquerda": importar_pasta("..","Grafismos","Personagem_Principal","Walk_Cycle","Esquerda")
            },
            "salto": {
                "direita": importar_pasta("..","Grafismos","Personagem_Principal","Jump_Cycle","Direita"),
                "esquerda": importar_pasta("..","Grafismos","Personagem_Principal","Jump_Cycle","Esquerda")
            },
            "pendurado": {
                "direita": importar_pasta("..","Grafismos","Personagem_Principal","Hang_Cycle","Direita"),
                "esquerda": importar_pasta("..","Grafismos","Personagem_Principal","Hang_Cycle","Esquerda")
            }
        }
        self.acção = "parado"
        self.lado = "direita"
        self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][self.indice_frame]
        self.rect = self.image.get_frect(center = pos)
        self.direção = vector()
    
    def movimentação(self, dt):
        self.rect.center += self.direção * 500 * dt

    def animação(self, dt):
        self.indice_frame += 4 * dt
        self.image = self.frames[self.acção][self.lado][int(self.indice_frame) % len(self.frames)]

    def update(self, dt):
        self.direção = input_jogador()
        self.movimentação(dt)
        self.animação(dt)