import pygame
import pygame_menu

from Screens.Creat_Account import create_account_menu
from Features.Dados_Verificacao import verificar_dados

pygame.init()
surface = pygame.display.set_mode((600, 400))

def login_screen(initial_screen):
    login_menu = pygame_menu.Menu(
        'Login',
        600,
        400,
        theme=pygame_menu.themes.THEME_SOLARIZED)

    nome_input = login_menu.add.text_input('Nome: ')
    email_input = login_menu.add.text_input('Email: ')
    senha_input = login_menu.add.text_input('Senha: ', password=True)

    screen = "logon"
    login_menu.add.button("Logar", verificar_dados,  nome_input,email_input,senha_input,screen)
    login_menu.add.button('Sair',  initial_screen, login_screen, create_account_menu)
    login_menu.mainloop(surface)