import pygame
from Loop_de_gestao_de_eventos import event_loop
pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
x, y = screen.get_size()

clock = pygame.time.Clock()

while True:
    event_loop()
    
    screen.fill('aqua')
    
    pygame.display.update()
    clock.tick(32)
