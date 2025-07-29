from Definições import *
from Personagem_Principal import Principal

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
        self.greetings = ["Ohoh! Bons olhos o vejam, meu velho!", "Em que posso ajudar?"]
        self.em_conversa = None
        self.tópicos_falados = []
    
    def início_conversa(self, target = "Conversa"):
        if not self.em_conversa:
            if target != "Conversa":
                if target == "Greeting":
                    self.em_conversa = DialogTree(target, (SCREEN_WIDTH/2,0), self.groups()[0], self.fim_conversa,
                                      custom_single=self.greetings)
                    print("here")
                    self.greetings = []
                else:
                    if target not in self.tópicos_falados:
                        self.em_conversa = DialogTree(target, (SCREEN_WIDTH/2,0), self.groups()[0], self.fim_conversa)
                        self.tópicos_falados.append(target)
                    else:
                        self.em_conversa = DialogTree(target, (SCREEN_WIDTH/2,0), self.groups()[0], self.fim_conversa, lastline=True)
            else:
                self.em_conversa = DialogTree(target, (SCREEN_WIDTH/2,0), self.groups()[0], self.fim_conversa)
    
    def fim_conversa(self, target):
        self.em_conversa = None
    
    def check_interação(self):
        if not self.em_conversa:
            if len(self.greetings) > 0:
                self.início_conversa("Greeting")
        jogador = [i for i in self.groups()[0].sprites() if isinstance(i, Principal)][0]
        itens_venda = [i for i in self.groups()[0].sprites()
                       if not isinstance(i, Principal) and hasattr(i, "tipo")]
        if jogador.rect.collidelist([i.rect for i in itens_venda]) > -1:
            if not self.em_conversa:
                item = itens_venda[jogador.rect.collidelist([i.rect for i in itens_venda])].tipo
                self.início_conversa(item)
        if jogador.interagir and jogador.rect.colliderect(self.rect):
            if not self.em_conversa:
                self.início_conversa()
    
    def animação(self, dt):
        jogador = [i for i in self.groups()[0].sprites() if isinstance(i, Principal)][0]
        if not self.em_conversa:
            self.acção = "parado"
        else:
            self.acção = "falar"
        if jogador.rect.centerx > self.rect.centerx:
            self.lado = "direita"
        else:
            self.lado = "esquerda"
        self.indice_frame += ANIMATION_SPEED * dt
        if int(self.indice_frame) >= len(self.frames[self.acção][self.lado]):
            self.indice_frame = 0
        self.image = self.frames[self.acção][self.lado][int(self.indice_frame)]

    def update(self, dt):
        self.check_interação()
        self.animação(dt)