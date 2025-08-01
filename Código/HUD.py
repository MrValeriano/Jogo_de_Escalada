from Definições import *

class HUD(pygame.sprite.Group):
    def __init__(self, player, testing):
        super().__init__()
        self.testing = testing
        
        self.font_moedas = fonts["HUD_moedas"]
        self.font_vidas = fonts["HUD_vidas"]
        self.font_size = fonts["HUD_vidas"].get_point_size()
        self.blink_direction = "red"
        self.hue = 255
        
        self.padding = 10
        self.escala = 2.5
        self.display_surf = pygame.display.get_surface()
        self.player = player
        
        self.item = self.player.inventário["Item"]
        self.n_vidas = self.player.inventário["Vidas"]
        self.n_moedas = self.player.inventário["Moedas"]
        
        #* Mochila
        self.mochila = pygame.image.load(join("Grafismos", "Itens", "Para_UI", "Mochila.png")).convert_alpha()
        if self.testing == False:
            self.mochila_rect = self.mochila.get_frect(bottomright = (SCREEN_WIDTH-self.padding, SCREEN_HEIGHT-self.padding))
        else:
            self.mochila_rect = self.mochila.get_frect(bottomleft = (self.padding, SCREEN_HEIGHT-self.padding))
        
        #* Coração
        vidas = pygame.image.load(join("Grafismos", "Itens", "Para_UI", "Coração.png")).convert_alpha()
        self.vidas_surf = pygame.transform.smoothscale(vidas, (vidas.width/self.escala, vidas.height/self.escala))
        
        if self.testing == False:
            self.vidas_rect = self.vidas_surf.get_frect(bottomleft = (self.padding, SCREEN_HEIGHT-self.padding))
        else:
            self.vidas_rect = self.vidas_surf.get_frect(bottomleft = (self.mochila_rect.bottomright + vector(self.padding, - self.padding)))
        
        #* Moeda
        moeda = pygame.image.load(join("Grafismos", "Itens", "Para_UI", "Moeda.png")).convert_alpha()
        self.moeda_surf = pygame.transform.smoothscale(moeda, (moeda.width/self.escala, moeda.height/self.escala))
        
        if self.testing == False:
            self.moeda_rect = self.moeda_surf.get_frect(bottomleft = (self.padding, (SCREEN_HEIGHT-self.vidas_rect.height)-self.padding))
        else:
            self.moeda_rect = self.moeda_surf.get_frect(topleft = (self.mochila_rect.topright + vector(self.padding, self.padding)))
    
    def blink(self, dt):
        if self.blink_direction == "white":
            self.hue += 50 * ANIMATION_SPEED * dt
            self.font_size -= 2*ANIMATION_SPEED * dt
        else:
            self.hue -= 50 * ANIMATION_SPEED * dt
            self.font_size += 2*ANIMATION_SPEED * dt
        if self.hue >= 255:
            self.hue = 255
            self.blink_direction = "red"
        elif self.hue <= 0:
            self.hue = 0
            self.blink_direction = "white"
        self.font_vidas.set_point_size(int(self.font_size))
        alt_surf = self.font_vidas.render(str(self.n_vidas), False, (255, int(self.hue), int(self.hue)))
        return alt_surf
    
    def obstruct(self):
        #* y = m*x + b
        #* m = (y2 - y1)/(x2 - x1)
        m = SCREEN_HEIGHT/SCREEN_WIDTH
        point_pairs = []
        stepx = 90
        for x in range(0, SCREEN_WIDTH, stepx):
            x1 = x
            y1 = 0
            y2 = SCREEN_HEIGHT
            x2 = ((y2 - y1) / m) + x1
            point_pairs.append([(x1, y1), (x2, y2)])
            x2 = ((y2 - y1) / (-m)) + x1
            point_pairs.append([(x1, y1), (x2, y2)])
        stepy = int(SCREEN_HEIGHT/(SCREEN_WIDTH/stepx))
        for y in range(0, SCREEN_HEIGHT, stepx-stepy):
            x1 = 0
            y1 = y
            y2 = SCREEN_HEIGHT
            x2 = (y2 - y1) / m
            point_pairs.append([(x1, y1), (x2, y2)])
            x1 = SCREEN_WIDTH
            y1 = y
            y2 = SCREEN_HEIGHT
            m = -m
            x2 = ((y2 - y1) / m) + x1
            point_pairs.append([(x1, y1), (x2, y2)])
        for pt in point_pairs:
            pygame.draw.line(self.display_surf, "#404040", pt[0], pt[1], 20)
    
    def draw(self, dt):
        #* Nº de moedas
        self.n_moedas_surf = self.font_moedas.render(str(self.n_moedas), False, "#ffffff")
        self.n_moedas_rect = self.n_moedas_surf.get_frect(midleft = self.moeda_rect.midright + vector(self.padding, 0))
        #* Nº de vidas
        if self.n_vidas < 2:
            self.n_vidas_surf = self.blink(dt)
        else:
            self.font_vidas.set_point_size(self.font_moedas.get_point_size())
            self.n_vidas_surf = self.font_vidas.render(str(self.n_vidas), False, "#ffffff")
        self.n_vidas_rect = self.n_vidas_surf.get_frect(midleft = self.vidas_rect.midright + vector(self.padding, 0))
        #* Drawing
        if self.item == "Apicultor":
            self.obstruct()
        self.display_surf.blits([(self.mochila, self.mochila_rect),
                                 (self.vidas_surf, self.vidas_rect),
                                 (self.moeda_surf, self.moeda_rect),
                                 (self.n_moedas_surf, self.n_moedas_rect),
                                 (self.n_vidas_surf, self.n_vidas_rect)])
        #* Item + Drawing
        if self.item != "":
            self.item_surf = pygame.image.load(join("Grafismos", "Itens", "Para_UI", f"{self.item}.png")).convert_alpha()
            self.item_rect = self.item_surf.get_frect(center = self.mochila_rect.center)
            self.display_surf.blit(self.item_surf, self.item_rect)
    
    def update(self):
        self.item = self.player.inventário["Item"]
        self.n_vidas = self.player.inventário["Vidas"]
        self.n_moedas = self.player.inventário["Moedas"]
