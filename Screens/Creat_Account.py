import pygame
import pygame_menu
from pygame_menu.examples.other.widget_positioning import label

from Features.Dados_Verificacao import DataVerifier

pygame.init()
surface = pygame.display.set_mode((600, 400))

def create_account_menu(initial_screen,login_screen):
    creat_menu = pygame_menu.Menu(
        'Criar Conta',
        600,
        400,
        theme=pygame_menu.themes.THEME_SOLARIZED)

    validator = DataVerifier("creat_account")

    nome_input = creat_menu.add.text_input('Nome: ')
    email_input = creat_menu.add.text_input('Email: ')
    senha_input = creat_menu.add.text_input('Senha: ', password=True)
    print(type(nome_input))
    creat_menu.add.button('Criar Conta',
                          validator.verify_data_for_create_login,
                          email_input,
                          senha_input,
                          nome_input,
                          None
                          )

    creat_menu.add.button('voltar', initial_screen, login_screen,create_account_menu)
    creat_menu.mainloop(surface)
