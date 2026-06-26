import pygame
import pygame_menu

from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from DataBase.repositories.difficulty_repository import DifficultyRepository
from models.user import User

pygame.init()
fundo = pygame.image.load('./Images/teladefundo.png')
def choice_difficulty(user:User, mod:str, tipo:str, tipo_2players=None):
    """
    Exibe a tela de seleção de dificuldade do jogo.
    
    Permite ao usuário escolher entre os níveis Easy, Normal e Hard,
    e navega para a tela de seleção de música com a dificuldade escolhida.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    from Screens.choice_music import choice_music
    from Screens.story_phase_select import story_phase_select 
    
    fundo = BaseImage(
        image_path="./Images/teladefundo.png",
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

    choice = pygame_menu.Menu(
        f' Connected as: {user.name}',
        width,
        height,
        theme=theme
    )
    
    difficultyManeger = DifficultyRepository()
    
    dificuldades = difficultyManeger.get_all()
    
    difficulty = dificuldades[0]
    def set_difficulty(value, selected_value):
        nonlocal  difficulty
        difficulty = selected_value
    
    choice.add.selector(
    "Select difficulty :", 
    [
        (dificuldades[0].name, dificuldades[0]),
        (dificuldades[1].name, dificuldades[1]),
        (dificuldades[2].name, dificuldades[2])
    ],
    onchange=set_difficulty
    )
    
    choice.add.label(
        "Each level has different sounds. The difficulty is based on the speed of the sound.", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )

    if tipo_2players:
        print(f"tipo_2player: {tipo_2players} mod: {mod}")
        choice.add.button("Continue", lambda: story_phase_select(user, difficulty, mod, tipo, tipo_2players))
    else:
        print(f"tipo: {tipo_2players} mod: {mod}")
        choice.add.button("Continue", lambda: story_phase_select(user, difficulty, mod, tipo))
    choice.add.button("BACK", home_screen, user, profile_options_menu)        
    choice.mainloop(surface)