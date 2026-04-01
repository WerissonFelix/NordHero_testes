import pygame
import pygame_menu
from pygame_menu.examples.other.widget_positioning import label

from Features.Dados_Verificacao import verificar_dados

pygame.init()
surface = pygame.display.set_mode((600, 400))

def create_account_menu(home_screen,initial_screen,login_screen):
    creat_menu = pygame_menu.Menu(
        'Criar Conta',
        600,
        400,
        theme=pygame_menu.themes.THEME_SOLARIZED)


    nome_input = creat_menu.add.text_input('Nome: ')
    email_input = creat_menu.add.text_input('Email: ')
    senha_input = creat_menu.add.text_input('Senha: ', password=True)

    screen = "creat_account"
    creat_menu.add.button('Criar Conta', verificar_dados,nome_input,email_input,senha_input,screen)

    creat_menu.add.button('voltar', initial_screen, login_screen,create_account_menu)
    creat_menu.mainloop(surface)
