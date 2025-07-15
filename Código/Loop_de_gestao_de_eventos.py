from Definições import *

def event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()