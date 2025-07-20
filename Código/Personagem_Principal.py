from Definições import *
from Processamento_do_input_do_jogador import input_jogador

class Principal(pygame.sprite.Sprite):
    def __init__(self, mapa, *groups):
        super().__init__(*groups)
        self.frames = {
            "parado": {
                "direita": importar_pasta("Grafismos","Personagem_Principal","Idle","Direita"),
                "esquerda": importar_pasta("Grafismos","Personagem_Principal","Idle","Esquerda")
            },
            "andar": {
                "direita": importar_pasta("Grafismos","Personagem_Principal","Walk_Cycle","Direita"),
                "esquerda": importar_pasta("Grafismos","Personagem_Principal","Walk_Cycle","Esquerda")
            },
            "salto": {
                "direita": importar_pasta("Grafismos","Personagem_Principal","Jump_Cycle","Direita"),
                "esquerda": importar_pasta("Grafismos","Personagem_Principal","Jump_Cycle","Esquerda")
            },
            "pendurado": {
                "direita": importar_pasta("Grafismos","Personagem_Principal","Hang_Cycle","Direita"),
                "esquerda": importar_pasta("Grafismos","Personagem_Principal","Hang_Cycle","Esquerda")
            }
        }
        self.acção = "parado"
        self.lado = "direita"
        self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][self.indice_frame]
        self.mapa = mapa
        self.rect = self.image.get_frect(center = self.mapa.posição)
        self.direção = vector()
        self.inventário = {
            "Moedas": 0,
            "Itens": [],
            "Vidas": 3
        }
    
    def movimentação(self, dt):
        self.rect.center += self.direção * 500 * dt

    def animação(self, dt):
        self.indice_frame += ANIMATION_SPEED * dt
        if int(self.indice_frame) >= len(self.frames[self.acção][self.lado]):
            self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][int(self.indice_frame)]
    
    def interação(self):
        print(self.rect.collidelist(self.mapa.lista_objectos["Moeda"]))
    
    def collisão(self):
        if self.rect.collidelist(self.mapa.lista_objectos["Moeda"]) > -1:
            moeda = self.rect.collidelist(self.mapa.lista_objectos["Moeda"])
            if self.mapa.lista_objectos["Moeda"][moeda].alive():
                self.mapa.lista_objectos["Moeda"][moeda].kill()
                self.inventário["Moedas"] += 1

    def update(self, dt):
        actividade = input_jogador()
        self.direção = actividade[0]
        if actividade[1] == "collect":
            self.interação()
        self.movimentação(dt)
        self.collisão()
        self.animação(dt)