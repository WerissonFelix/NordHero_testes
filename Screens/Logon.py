import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from Screens.Creat_Account import create_account_menu
from Features.Dados_Verificacao import DataVerifier

pygame.init()
surface = pygame.display.set_mode((800, 500))

def login_screen(initial_screen):
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_BEBAS
    
    fundo_login = BaseImage(
        image_path="teladefundo.png",
        drawing_mode=IMAGE_MODE_FILL
    )

    theme.background_color = fundo_login

    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior
    theme.title_background_color = (0, 0, 0)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (350, 0)

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