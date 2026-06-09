import pygame
import pygame_menu
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL
from Game.GameManager.GameManager import ManageGame
from models.user import User
pygame.init()
fundo = pygame.image.load('./Images/teladefundo.png')

def codigo_email(screen_name: str, codigo):

    from Screens.Home import home_screen

    fundo = BaseImage(
        image_path="./Images/teladefundo.png",
        drawing_mode=IMAGE_MODE_FILL
    )
    theme = pygame_menu.themes.THEME_DARK.copy()
  
    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior 
    theme.background_color = fundo 
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (10, 50)

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    resultado = None

    def verificar_codigo():
        nonlocal resultado
        resultado = codigo_input.get_value()
        code_menu.disable()
        
    surface = pygame.display.get_surface()
    width, height = surface.get_size()

    code_menu = pygame_menu.Menu(
        "",
        width, 
        height,
        theme=theme
        )
    
    codigo_input = code_menu.add.text_input('Code: ', maxchar=20)

    code_menu.add.button("CONFIRM", verificar_codigo)
    code_menu.add.button("EXIT", pygame_menu.events.EXIT)
    code_menu.mainloop(surface)

    return resultado