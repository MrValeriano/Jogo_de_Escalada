from Definições import *
from Mapa import *
from Loop_de_gestao_de_eventos import event_loop
from Personagem_Principal import *

jogador = pygame.sprite.GroupSingle()
jogador.add(Principal())

while True:
    event_loop()
    screen.fill('aqua')
    
    jogador.draw(screen)
    
    pygame.display.update()
    clock.tick(32)
