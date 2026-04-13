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
        image_path="teladefundo.png",
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
        'Dados invalidos',
        800,
        500,
        theme = theme
    )
    
    error_menu.add.label(erro_message)


    if screen_error_name.lower() == 'logon':
        error_menu.add.button("voltar", Logon.login_screen, Inital.initial_screen)
    else:
        error_menu.add.button("voltar", Creat_Account.create_account_menu, Inital.initial_screen, Logon.login_screen)

    error_menu.mainloop(surface)
