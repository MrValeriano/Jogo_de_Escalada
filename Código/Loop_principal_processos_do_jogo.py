from Definições import *
from Mapa import *
from Loop_de_gestao_de_eventos import event_loop
from Personagem_Principal import *

jogador = pygame.sprite.GroupSingle()
jogador.add(Principal())

while True:
    #* tick
    dt = clock.tick()/1000
    #* eventos
    event_loop()
    #* representações no ecrã
    todos_sprites.update(dt)
    screen.fill('aqua')
    todos_sprites.draw(screen)
    jogador.draw(screen)
    
    pygame.display.update()
