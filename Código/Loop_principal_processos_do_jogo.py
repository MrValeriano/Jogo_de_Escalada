from Definições import *
from Mapa import *
from Itens import *
from NPCs import *
from Inimigos import *
from Loop_de_gestao_de_eventos import event_loop
from Personagem_Principal import *

mapa = Mapa()
jogador = Principal(mapa.posição, todos_sprites)

while True:
    #* tick
    dt = clock.tick()/1000
    #* eventos
    event_loop()
    #* representações no ecrã
    todos_sprites.update(dt)
    screen.fill('aqua')
    todos_sprites.draw(jogador.rect.center)
    
    pygame.display.update()
