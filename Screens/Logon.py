import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from Screens.Creat_Account import create_account_menu
from Features.Dados_Verificacao import DataVerifier
from models.user import User

pygame.init()
surface = pygame.display.set_mode((800, 500))

def login_screen(initial_screen):
    """
    Exibe o formulário de login do usuário.
    
    Coleta email e senha para autenticação e valida as credenciais
    do usuário no sistema.
    """
    
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_BEBAS
    
    fundo_login = BaseImage(
        image_path="./Images/TelaLogin.png",
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
        '',
        800,
        500,

    theme=theme)

    validator = DataVerifier("logon")

    email_input = login_menu.add.text_input('Email: ', maxchar=20)
    email_input.set_alignment(pygame_menu.locals.ALIGN_LEFT)
    email_input.translate(180, 0)

    senha_input = login_menu.add.text_input('Password: ', password=True, maxchar=20)
    senha_input.set_alignment(pygame_menu.locals.ALIGN_LEFT)
    senha_input.translate(180, 0)

    
    def login_callback():
        nonlocal email_input
        user = User(None, None, email_input.get_value(), senha_input.get_value())
        validator.verify_data_for_create_login(user)
        
    login_menu.add.button("LOGIN", login_callback)
    login_menu.add.button('EXIT',  initial_screen, login_screen, create_account_menu)

    login_menu.mainloop(surface)