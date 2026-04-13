import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from Screens.Home import home_screen
from DataBase.deletes import delete_user

pygame.init()
surface = pygame.display.set_mode((600, 400))

def delete_menu(user, profile_options):
    
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_BEBAS
    
    fundo_delete_menu = BaseImage(
        image_path="TelaDeleteAccount.png",
        drawing_mode=IMAGE_MODE_FILL
    )

    theme.background_color = fundo_delete_menu

    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior
    theme.title_background_color = (0, 0, 0)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (350, 0)

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    delete  = pygame_menu.Menu(
        '',
        800,
        500,

        theme=theme)

    delete.add.button("Delete", delete_user, user[0], user[2])
    delete.add.button('Back', profile_options, user)

    delete.mainloop(surface)

"""
def teste():
    from tkinter import *
    from tkinter import messagebox
    Tk().wm_withdraw()  # to hide the main window
    messagebox.showinfo('Continue', 'OK')
"""
