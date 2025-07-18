from Definições import *
from Mapa import *
from Itens import *
from NPCs import *
from Inimigos import *
from Loop_de_gestao_de_eventos import event_loop
from Personagem_Principal import *

mapa = Mapa()
jogador = Principal(mapa.posição, todos_sprites)
tarta = Inimigo((0,0),"Tartaruga",1)

while True:
    #* tick
    dt = clock.tick()/2000
    #* eventos
    event_loop()
    #* representações no ecrã
    todos_sprites.update(dt)
    screen.fill('black')
    todos_sprites.draw(jogador.rect.center)
    
    tarta.update(dt)
    
    pygame.display.update()
