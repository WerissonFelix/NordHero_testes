import pygame
import pygame_menu
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL
from Game.GameManager.GameManager import ManageGame
from models.user import User
pygame.init()
fundo = pygame.image.load('./Images/TelaPadrao.png')

def home_screen(user : User, profile_menu):
    """
    Exibe a tela principal do jogo após o login.
    
    Mostra informações do usuário conectado e oferece opções para
    iniciar o jogo, acessar configurações ou sair do sistema.
    """
    
    from Screens.choice_mod import choice_mod
    from Screens.history_screen import history_screen
    from Screens.estatisticas import estatisticas_screen
    from Screens.AI_analise import AI_analise
    from Screens.achievements import achievements_screen
    
    fundo = BaseImage(
        image_path="./Images/TelaPadrao.png",
        drawing_mode=IMAGE_MODE_FILL
    )
    theme = pygame_menu.themes.THEME_DARK.copy()

    #Fonte e Tamanho do nome "Conectado como: {user[1]}"
    theme.title_font = pygame_menu.font.FONT_MUNRO
    theme.title_font_size = 20
    
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

    home_menu = pygame_menu.Menu(
        '',
        width,
        height,
        theme=theme
    )
    
   # 1. Criamos cada informação como um texto separado, definindo a nova fonte
    lbl_nome = home_menu.add.label(
        f"Name: {user.name}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    lbl_email = home_menu.add.label(
        f"email: {user.email}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
   
    lbl_nome.set_float(True)
    lbl_nome.set_alignment(ALIGN_RIGHT)
    lbl_nome.translate(-20, -160)

    lbl_email.set_float(True)
    lbl_email.set_alignment(ALIGN_RIGHT)
    lbl_email.translate(-20, -135)

    lbl_nome.set_float(True)
    lbl_nome.set_alignment(ALIGN_RIGHT)
    lbl_nome.translate(-20, -160)

    home_menu.add.button("START", choice_mod, user)
    home_menu.add.button("HISTORY", history_screen, user)
    home_menu.add.button("SETTINGS", profile_menu, user)
    home_menu.add.button("STATICTICS", estatisticas_screen, user)
    home_menu.add.button("AI ANALYTICS", AI_analise, user)
    home_menu.add.button("ACHIEVEMENTS", achievements_screen, user)
    home_menu.add.button("EXIT", pygame_menu.events.EXIT)
    home_menu.mainloop(surface)