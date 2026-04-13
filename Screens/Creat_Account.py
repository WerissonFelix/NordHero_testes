import pygame
import pygame_menu
from pygame_menu.examples.other.widget_positioning import label

from Features.Dados_Verificacao import DataVerifier

pygame.init()
surface = pygame.display.set_mode((600, 400))

def create_account_menu(initial_screen,login_screen):
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_OPEN_SANS

    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior
    theme.title_background_color = (75, 0, 130)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    creat_menu = pygame_menu.Menu(
        'Criar Conta',
        800,
        500,
        theme=theme)

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
