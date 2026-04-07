import pygame
import pygame_menu

from Screens import Home, Logon, Creat_Account, Inital

pygame.init()
surface = pygame.display.set_mode((600, 400))

def data_error_screen(erro_mensage,screen_error_name):
    error_menu = pygame_menu.Menu(
        'Dados inválidos',
        600,
        400,
        theme=pygame_menu.themes.THEME_SOLARIZED)

    error_menu.add.label(erro_mensage)

    screens_names = ["logon","creat_account"]

    if screen_error_name in screens_names:
        if screen_error_name.lower() == 'logon':
            error_menu.add.button("voltar", Logon.login_screen, Inital.initial_screen)
        else:
            error_menu.add.button("voltar", Creat_Account.create_account_menu, Inital.initial_screen, Logon.login_screen)
    else:
        error_menu.add.label("Erro não esperado, por favor, reinicie o jogo")
        error_menu.add.button("Fechar jogo", pygame_menu.events.EXIT)

    error_menu.mainloop(surface)
