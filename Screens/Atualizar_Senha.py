import pygame
import pygame_menu
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL
from Game.GameManager.GameManager import ManageGame
from models.user import User
pygame.init()
fundo = pygame.image.load('./Images/teladefundo.png')

def atualizar_senha(user: User):
    from Screens.Home import home_screen
    from Features.Dados_Verificacao import DataVerifier
    from Screens.update_screen import update_menu
    from Screens.profile_options import profile_options_menu

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

    surface = pygame.display.get_surface()
    width, height = surface.get_size()

    attsenha_menu = pygame_menu.Menu(
        "",
        width,
        height,
        theme=theme
    )
   
    validator = DataVerifier("update_screen")
    def update_callback():
        new_user = User(user.id, user.name, user.email, senha_input.get_value())
        validator.verify_just_for_update(new_user)

    senha_input = attsenha_menu.add.text_input('New Password: ', maxchar=20, password=True)

    attsenha_menu.add.button("CONFIRM", update_callback)
    attsenha_menu.add.button("EXIT", update_menu,user, profile_options_menu)
    attsenha_menu.mainloop(surface)
