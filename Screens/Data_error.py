import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from Screens import Home, Logon, Creat_Account, Inital, update_screen, profile_options

pygame.init()
surface = pygame.display.set_mode((600, 400))

def data_error_screen(erro_message,screen_error_name, user = None):
    """
    Exibe uma tela de erro com mensagens personalizadas.
    
    Mostra os erros encontrados durante operações e fornece
    navegação de volta para a tela apropriada conforme o contexto do erro.
    
    """
    
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_background_color = (0, 0, 0)
    theme.title_font = pygame_menu.font.FONT_BEBAS
    
    fundo_error = BaseImage(
        image_path="./Images/TelaDataError.png",
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
    elif screen_error_name.lower() == "creat_account":
        error_menu.add.button("BACK", Creat_Account.create_account_menu, Inital.initial_screen, Logon.login_screen)
    else:
        error_menu.add.button("BACK", update_screen.update_menu, user, profile_options.profile_options_menu)
    error_menu.mainloop(surface)