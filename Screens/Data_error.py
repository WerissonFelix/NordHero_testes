import pygame
import pygame_menu

from Screens import Home, Logon, Creat_Account, Inital

pygame.init()
surface = pygame.display.set_mode((600, 400))

def data_error_screen(erro_message,screen_error_name):
    error_menu = pygame_menu.Menu(
        'Dados inválidos',
        600,
        400,
        theme=pygame_menu.themes.THEME_SOLARIZED)

    error_menu.add.label(erro_message)


    if screen_error_name.lower() == 'logon':
        error_menu.add.button("voltar", Logon.login_screen, Inital.initial_screen)
    else:
        error_menu.add.button("voltar", Creat_Account.create_account_menu, Inital.initial_screen, Logon.login_screen)

    error_menu.mainloop(surface)
