import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

pygame.init()
surface = pygame.display.set_mode((800, 500))
fundo = pygame.image.load("./Images/telainicial.png")

def initial_screen(login_screen,create_account_menu):
    fundo = BaseImage(
        image_path="./Images/telainicial.png",
        drawing_mode=IMAGE_MODE_FILL
    )
    theme = pygame_menu.themes.THEME_DARK.copy()
    
    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior
    theme.background_color = fundo
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (290, 0)

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    initial_menu = pygame_menu.Menu(
        '',
        800,
        500,
        theme=theme )

    initial_menu.add.button('LOGIN', login_screen,initial_screen)
    initial_menu.add.button('CREATE ACCOUNT', create_account_menu,initial_screen, login_screen) 
    initial_menu.add.button('EXIT', pygame_menu.events.EXIT) 

    initial_menu.mainloop(surface)