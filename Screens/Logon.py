import pygame
import pygame_menu

from Screens.Creat_Account import create_account_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))

def login_screen(home_screen,initial_screen):
    login_menu = pygame_menu.Menu(
        'Login',
        400,
        300,
        theme=pygame_menu.themes.THEME_BLUE)


    nome_input = login_menu.add.text_input('Nome: ', default='Carlos')
    email_input = login_menu.add.text_input('Email  : ', default='Carlos@gmail.com')

    dados = {"nome": nome_input.get_value(), "email": email_input.get_value()}

    login_menu.add.button("Logar", home_screen, dados)
    login_menu.add.button('Sair',  initial_screen, login_screen, create_account_menu)
    login_menu.mainloop(surface)