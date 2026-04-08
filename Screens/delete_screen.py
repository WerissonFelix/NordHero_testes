import pygame
import pygame_menu

from Screens.Home import home_screen
from DataBase.deletes import delete_user

pygame.init()
surface = pygame.display.set_mode((600, 400))

def delete_menu(user, profile_options):
    delete  = pygame_menu.Menu(
        'Atualizar dados',
        600,
        400,

        theme=pygame_menu.themes.THEME_SOLARIZED)

    delete.add.button("Deletar", delete_user, user[0], user[2])
    delete.add.button('Voltar', profile_options, user)

    delete.mainloop(surface)

"""
def teste():
    from tkinter import *
    from tkinter import messagebox
    Tk().wm_withdraw()  # to hide the main window
    messagebox.showinfo('Continue', 'OK')
"""
