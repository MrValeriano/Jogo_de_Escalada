from Definições import *
from sys import exit

def event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == GAME_OVER:
            print("\n\nGame Over, baby!")
            pygame.quit()
            exit()