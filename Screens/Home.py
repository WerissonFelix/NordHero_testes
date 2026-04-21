import pygame
import pygame_menu
from Game.GameManager.GameManager import ManageGame

pygame.init()
surface = pygame.display.set_mode((600, 400))

def home_screen(user,profile_menu):
    home_menu = pygame_menu.Menu(
        f'Bem-vindo, {user[1]}',
        600,
        400,
        theme=pygame_menu.themes.THEME_BLUE)

    home_menu.add.label(
        f"""Name: {user[1]}
                email: {user[2]}
                password: {user[3]}
            """, font_size=30)
    
    testee = ManageGame()
    
    home_menu.add.button("iniciar", testee.load_to_run)
    home_menu.add.button("Configurações", profile_menu, user)
    home_menu.add.button("Sair do Jogo", pygame_menu.events.EXIT)
    home_menu.mainloop(surface)