import pygame
import pygame_menu


pygame.init()
surface = pygame.display.set_mode((600, 400))

def home_screen(lista):
    home_menu = pygame_menu.Menu(
        f'Bem-vindo {lista["nome"]}',
        400,
        300,
        theme=pygame_menu.themes.THEME_BLUE)

    home_menu.add.label("Press ESC to exit", font_size=20)

    home_menu.add.button("iniciar")
    home_menu.add.button("Configurações")
    home_menu.add.button("Sair do Jogo", pygame_menu.events.EXIT)
    home_menu.mainloop(surface)