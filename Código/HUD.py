from Definições import *

class HUD(pygame.sprite.Group):
    def __init__(self, player):
        super().__init__()
        self.font = fonts["HUD"]
        
        self.padding = 10
        self.display_surf = pygame.display.get_surface()
        self.player = player
        
        self.item = self.player.inventário["Item"]
        self.n_vidas = self.player.inventário["Vidas"]
        self.n_moedas = self.player.inventário["Moedas"]
        
        #* Mochila
        self.mochila = pygame.image.load(join("Grafismos", "Itens", "Para_UI", "Mochila.png")).convert_alpha()
        self.mochila_rect = self.mochila.get_frect(bottomright = (SCREEN_WIDTH-self.padding, SCREEN_HEIGHT-self.padding))
        
        #* Coração
        vidas = pygame.image.load(join("Grafismos", "Itens", "Para_UI", "Coração.png")).convert_alpha()
        self.vidas_surf = pygame.transform.smoothscale(vidas, (vidas.width/2, vidas.height/2))
        self.vidas_rect = self.vidas_surf.get_frect(bottomleft = (self.padding, SCREEN_HEIGHT-self.padding))
        
        #* Moeda
        moeda = pygame.image.load(join("Grafismos", "Itens", "Para_UI", "Moeda.png")).convert_alpha()
        self.moeda_surf = pygame.transform.smoothscale(moeda, (moeda.width/2, moeda.height/2))
        self.moeda_rect = self.moeda_surf.get_frect(bottomleft = (self.padding, (SCREEN_HEIGHT-self.vidas_rect.height)-self.padding))
    
    def draw(self):
        self.n_moedas_surf = self.font.render(self.n_moedas, False, "#ffffff")
        width = max(200, self.n_moedas_surf.get_width() + self.padding * 2)
        height = self.n_moedas_surf.get_height() + self.padding * 2
        
        self.display_surf.blits([(self.mochila, self.mochila_rect),
                                 (self.vidas_surf, self.vidas_rect),
                                 (self.moeda_surf, self.moeda_rect)])
        #* Item
        if self.item != "":
            self.item_surf = pygame.image.load(join("Grafismos", "Itens", "Para_UI", f"{self.item}.png")).convert_alpha()
            self.item_rect = self.item_surf.get_frect(bottomright = (SCREEN_WIDTH-self.padding, SCREEN_HEIGHT-self.padding))
            self.display_surf.blit(self.inventário, self.inventário_rect)
    
    def update(self):
        self.item = self.player.inventário["Item"]
        self.n_vidas = self.player.inventário["Vidas"]
        self.n_moedas = self.player.inventário["Moedas"]
        
    
    
class HUD_Element:
    def __init__(self, msg, pos, font, *groups):
        super().__init__(*groups)
        #* texto
        text_surf = font.render(msg, False, "black")
        padding = 15
        width = max(200, text_surf.get_width() + padding * 2)
        height = text_surf.get_height() + padding * 2
        #* fundo
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill((0,0,0,0))
        pygame.draw.rect(surf, "#ffffff", surf.get_frect(topleft = (0,0)), 0, 10)
        surf.blit(text_surf, text_surf.get_frect(center = (width/2, height/2)))
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos + vector(0, -10))