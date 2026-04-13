import pygame
import pygame_menu

from Screens.Home import home_screen
from DataBase.deletes import delete_user

pygame.init()
surface = pygame.display.set_mode((600, 400))

def delete_menu(user, profile_options):
    delete  = pygame_menu.Menu(
        'Update data',
        800,
        500,

        theme=pygame_menu.themes.THEME_DARK)

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
