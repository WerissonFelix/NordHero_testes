import pygame
import pygame_menu

from Screens.Creat_Account import create_account_menu
from Features.Dados_Verificacao import DataVerifier

pygame.init()
surface = pygame.display.set_mode((600, 400))

def login_screen(initial_screen):
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_background_color = (75, 0, 130)
    theme.title_font = pygame_menu.font.FONT_OPEN_SANS

    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior
    theme.title_background_color = (75, 0, 130)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    login_menu = pygame_menu.Menu(
        'Login',
        800,
        500,

        theme=theme)

    validator = DataVerifier("logon")
    email_input = login_menu.add.text_input('Email: ')
    senha_input = login_menu.add.text_input('Senha: ', password=True)

    login_menu.add.button("Logar", validator.verify_data_for_create_login, email_input, senha_input, None, None)
    login_menu.add.button('Sair',  initial_screen, login_screen, create_account_menu)

    login_menu.mainloop(surface)