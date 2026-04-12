import pygame
import pygame_menu

from Screens.Creat_Account import create_account_menu
from Features.Dados_Verificacao import DataVerifier

pygame.init()
surface = pygame.display.set_mode((600, 400))

def login_screen(initial_screen):
    login_menu = pygame_menu.Menu(
        'Login',
        600,
        400,

        theme=pygame_menu.themes.THEME_SOLARIZED)

    validator = DataVerifier("logon")
    email_input = login_menu.add.text_input('Email: ')
    senha_input = login_menu.add.text_input('Senha: ', password=True)

    login_menu.add.button("Logar", validator.verify_data_for_create_login, email_input, senha_input, None, None)
    login_menu.add.button('Sair',  initial_screen, login_screen, create_account_menu)

    login_menu.mainloop(surface)