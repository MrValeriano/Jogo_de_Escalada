from Definições import *

imagem_moeda = pygame.image.load(join("Grafismos", "Itens", "Moeda", "0.png")).convert_alpha()
ui_moeda = pygame.transform.smoothscale(imagem_moeda, (2*imagem_moeda.width/3, 2*imagem_moeda.height/3))
rect_moeda = ui_moeda.get_frect(bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT))