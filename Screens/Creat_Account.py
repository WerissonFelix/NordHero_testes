import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL
from pygame_menu.examples.other.widget_positioning import label

from Features.Dados_Verificacao import DataVerifier

pygame.init()
surface = pygame.display.set_mode((600, 400))

def create_account_menu(initial_screen,login_screen):
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_BEBAS

    fundo_criar_conta = BaseImage(
        image_path="./Images/TelaCreateAccount.png",
        drawing_mode=IMAGE_MODE_FILL
    )

    theme.background_color = fundo_criar_conta
    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior
    theme.title_background_color = (0, 0, 0)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (290, 0)

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    creat_menu = pygame_menu.Menu(
        '',
        800,
        500,
        theme=theme)

    validator = DataVerifier("creat_account")

    nome_input = creat_menu.add.text_input('Name: ')
    nome_input.set_alignment(pygame_menu.locals.ALIGN_LEFT)
    nome_input.translate(180, 0)

    email_input = creat_menu.add.text_input('Email: ')
    email_input.set_alignment(pygame_menu.locals.ALIGN_LEFT)
    email_input.translate(180, 0)

    senha_input = creat_menu.add.text_input('Password: ', password=True)
    senha_input.set_alignment(pygame_menu.locals.ALIGN_LEFT)
    senha_input.translate(180, 0)

    print(type(nome_input))
    creat_menu.add.button('CREATE ACCOUNT',
                          validator.verify_data_for_create_login,
                          email_input,
                          senha_input,
                          nome_input,
                          None
                          )

    creat_menu.add.button('BACK', initial_screen, login_screen,create_account_menu)
    creat_menu.mainloop(surface)
