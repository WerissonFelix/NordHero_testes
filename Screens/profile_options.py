import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from Screens.Home import home_screen
from Screens.update_screen import update_menu
from Screens.delete_screen import delete_menu

pygame.init()
surface = pygame.display.set_mode((800, 500))

def profile_options_menu(user):
    
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_BEBAS
    
    fundo_profile_options = BaseImage(
        image_path="TelaProfileMenu.png",
        drawing_mode=IMAGE_MODE_FILL
    )

    theme.background_color = fundo_profile_options

    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

        #Cor e Estilo da Barra Superior
    theme.title_background_color = (0, 0, 0)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (290, 0)

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
    options = pygame_menu.Menu(
        '',
        800,
        500,

        theme=theme)

    options.add.button("Update data", update_menu , user,profile_options_menu)
    options.add.button("Delete Account", delete_menu, user, profile_options_menu)
    options.add.button('Back', home_screen, user,profile_options_menu)

    options.mainloop(surface)