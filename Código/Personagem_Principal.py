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
        self.dano = False
        self.acção = "parado"
        self.lado = "direita"
        self.indice_frame = 0
        self.frames_invencibilidade = 0
        self.tempo_invencibilidade = 0
        self.image = self.frames[self.acção][self.lado][self.indice_frame]
        self.mapa = mapa
        self.rect = self.image.get_frect(center = self.mapa.posição)
        self.direção = vector()
        self.relógio_interno = pygame.time.Clock()
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
        if self.dano == True:
            self.frames_invencibilidade += ANIMATION_SPEED * dt
            if int(self.frames_invencibilidade) % 4 == 0:
                self.image.set_alpha(0)
            else:
                self.image.set_alpha(255)
        else:
            self.frames_invencibilidade = 0
            self.image.set_alpha(255)
    
    def interacção(self):
        self.rect.collidelist(self.mapa.lista_objectos["Moeda"])
        print(self.inventário)
    
    def collisão_entidades(self):
        if self.rect.collidelist(self.mapa.lista_objectos["Moeda"]) > -1:
            moeda = self.rect.collidelist(self.mapa.lista_objectos["Moeda"])
            if self.mapa.lista_objectos["Moeda"][moeda].alive():
                self.mapa.lista_objectos["Moeda"][moeda].kill()
                self.inventário["Moedas"] += 1
        if self.dano == False:
            if self.rect.collidelist(self.mapa.lista_objectos["Vespa"]) > -1:
                if self.dano == False:
                    self.dano = True
                    self.inventário["Vidas"] -= 1
            if self.rect.collidelist(self.mapa.lista_objectos["Tartaruga"]) > -1:
                if self.dano == False:
                    self.dano = True
                    self.inventário["Vidas"] -= 1
    
    def verificar_estado(self):
        if self.dano == True:
            self.tempo_invencibilidade += self.relógio_interno.tick()/1000
            if int(self.tempo_invencibilidade) >= 3:
                self.tempo_invencibilidade = 0
                self.dano = False
        if self.inventário["Vidas"] == 0:
            print("GAME OVER")

    def update(self, dt):
        self.verificar_estado()
        input_jogador(self)
        self.movimentação(dt)
        self.collisão_entidades()
        self.animação(dt)