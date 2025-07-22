from Definições import *

imagem_moeda = pygame.image.load(join("Grafismos", "Itens", "Moeda", "0.png")).convert_alpha()
ui_moeda = pygame.transform.smoothscale(imagem_moeda, (imagem_moeda.width/2, imagem_moeda.height/2))
rect_moeda = ui_moeda.get_frect(bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT))