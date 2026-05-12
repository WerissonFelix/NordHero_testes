import pygame
import pygame_menu
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL
from Game.GameManager.GameManager import ManageGame
from models.user import User
pygame.init()
surface = pygame.display.set_mode((800, 500))
fundo = pygame.image.load('./Images/telainicial.png')
def choice_difficulty(user:User):
    """
    Exibe a tela de seleção de dificuldade do jogo.
    
    Permite ao usuário escolher entre os níveis Easy, Normal e Hard,
    e navega para a tela de seleção de música com a dificuldade escolhida.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    from Screens.choice_music import choice_music
    
    fundo = BaseImage(
        image_path="./Images/telainicial.png",
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

    choice = pygame_menu.Menu(
        f'Connected as: {user.name}',
        800,
        500,
        theme=theme
        )
    
   # 1. Criamos cada informação como um texto separado, definindo a nova fonte
    lbl_nome = choice.add.label(
        f"Name: {user.name}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    lbl_email = choice.add.label(
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
    
    difficulty = 'Easy'
    def set_difficulty(value, selected_value):
        nonlocal  difficulty
        difficulty = selected_value
        
    choice.add.selector(
    "Select difficulty :", 
    [
        ('Easy', 'Easy'),
        ('Normal', 'Normal'),
        ('Hard', 'Hard')
    ],
    onchange=set_difficulty
    )
    
    choice.add.label(
        "Each level has different sounds. The difficulty is based on the speed of the sound.", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )

    choice.add.button("Continue", lambda: choice_music(user, difficulty))
    choice.add.button("BACK", home_screen, user, profile_options_menu)        
    choice.mainloop(surface)