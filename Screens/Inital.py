import pygame
import pygame_menu

from Screens.Home import home_screen

pygame.init()
surface = pygame.display.set_mode((600, 400))

def initial_screen(login_screen,create_account_menu):
    initial_menu = pygame_menu.Menu(
        'Bem-vindo',
        400,
        300,
        theme=pygame_menu.themes.THEME_BLUE)

    initial_menu.add.button('Login', login_screen,home_screen,initial_screen)
    initial_menu.add.button('Criar Conta', create_account_menu,home_screen,initial_screen, login_screen)
    initial_menu.add.button('Sair', pygame_menu.events.EXIT)

    initial_menu.mainloop(surface)
