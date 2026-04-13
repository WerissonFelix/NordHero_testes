import pygame
import pygame_menu

from Screens.Home import home_screen
from Screens.update_screen import update_menu
from Screens.delete_screen import delete_menu

pygame.init()
surface = pygame.display.set_mode((800, 500))

def profile_options_menu(user):
    options = pygame_menu.Menu(
        'Profile Options',
        800,
        500,

        theme=pygame_menu.themes.THEME_DARK)

    options.add.button("Atualizar dados", update_menu , user,profile_options_menu)
    options.add.button("Deletar Conta", delete_menu, user, profile_options_menu)
    options.add.button('Voltar', home_screen, user,profile_options_menu)

    options.mainloop(surface)