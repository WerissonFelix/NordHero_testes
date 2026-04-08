import pygame
import pygame_menu

from Screens.Home import home_screen
from Screens.update_screen import update_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))

def profile_options_menu(user):
    options = pygame_menu.Menu(
        'Atualizar dados',
        600,
        400,

        theme=pygame_menu.themes.THEME_SOLARIZED)

    options.add.button("Atualizar dados", update_menu , user )
    options.add.button('Voltar', home_screen, user,)

    options.mainloop(surface)