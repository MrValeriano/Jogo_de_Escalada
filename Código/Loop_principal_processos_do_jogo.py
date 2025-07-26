from Definições import *
from Display import *
from Mapa import *
from Itens import *
from NPCs import *
from Inimigos import *
from Loop_de_gestao_de_eventos import event_loop
from Personagem_Principal import *

mapa = Mapa()
clock.tick()
jogador = Principal(mapa, todos_sprites)        

while True:
    #* tick
    dt = clock.tick()/1000
    screen.fill('black')
    #* eventos
    event_loop()
    #* verificações & updates
    mapa.check_transição(jogador)
    todos_sprites.update(dt)
    #* representações no ecrã
    todos_sprites.draw(jogador.rect.center)
    
    mapa.fade(dt, jogador)
    print(jogador.rect.center, dt)
    pygame.display.update()
