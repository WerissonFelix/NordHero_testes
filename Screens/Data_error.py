import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from Screens import Home, Logon, Creat_Account, Inital

pygame.init()
surface = pygame.display.set_mode((600, 400))

def data_error_screen(erro_message,screen_error_name):
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_background_color = (0, 0, 0)
    theme.title_font = pygame_menu.font.FONT_BEBAS
    
    fundo_error = BaseImage(
        image_path="TelaDataError.png",
        drawing_mode=IMAGE_MODE_FILL
    )

    theme.background_color = fundo_error

    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    #Cor e Estilo da Barra Superior 
    theme.background_color = fundo_error
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (260, 0)

    error_menu = pygame_menu.Menu(
        '',
        800,
        500,
        theme = theme
    )
    
    if isinstance(erro_message, list):
        for erro in erro_message:
            error_menu.add.label(erro, font_size=25, font_color=(255, 50, 50))
    else:
        error_menu.add.label(erro_message, font_size=25, font_color=(255, 50, 50))
    error_menu.add.vertical_margin(25)

    if screen_error_name.lower() == 'logon':
        error_menu.add.button("BACK", Logon.login_screen, Inital.initial_screen)
    else:
        error_menu.add.button("BACK", Creat_Account.create_account_menu, Inital.initial_screen, Logon.login_screen)

    error_menu.mainloop(surface)
