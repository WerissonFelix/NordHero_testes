import pygame
import pygame_menu
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL
from Game.GameManager.GameManager import ManageGame

pygame.init()
surface = pygame.display.set_mode((800, 500))
fundo = pygame.image.load('./Images/telainicial.png')
music = ""
def choice_music(user, difficulty_level):
    """
    Exibe a tela de seleção de música baseada na dificuldade escolhida.
    
    Apresenta diferentes listas de músicas conforme o nível de dificuldade
    e permite iniciar o jogo com a música selecionada.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    
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
        f'Connected as: {user[1]}',
        800,
        500,
        theme=theme
        )
    
   # 1. Criamos cada informação como um texto separado, definindo a nova fonte
    lbl_nome = choice.add.label(
        f"Name: {user[1]}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    lbl_email = choice.add.label(
        f"email: {user[2]}", 
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
    
    selected_music = [None] 
    
    def start_game(music_selector):
        if selected_music[0] is None:
            selected_music[0] = music_selector.get_value()[0][1]
        
        gameManager = ManageGame(user,selected_music[0])
        gameManager.load_to_run()
    print(difficulty_level)
    if difficulty_level == "Easy":
        music_selector = choice.add.selector(
            'MUSIC :', 
            [
            ('Die With Smile', "Game\music\Die With A Smile (Instrumental) - Lady Gaga"), 
            ('Ludovico Einaudi - Una Mattina', "Game\music\Ludovico Einaudi - Una Mattina (The Intouchables) - Rousseau (youtube)"), 
            ('Debussy - Clair de Lune - Rousseau', "Game\music\Debussy - Clair de Lune - Rousseau (youtube)")
            ],
            onchange=music)
        
    elif difficulty_level == "Normal":
        music_selector = choice.add.selector(
            'MUSIC :', 
            [
            ('Billie Jean', "Game\music\Michael Jackson  Billie Jean [Instrumental Version] - HIStoryWorldTourMJ (youtube)"), 
            ('Stay With me', "Game\music\Miki Matsubara - Stay With Me"), 
            ("Another One Bites The Dust - Queen", "Game\music\Another One Bites The Dust - Instrumental"),
            ('Fallen Down - toby Fox', "Game\music\Fallen Down (Reprise) - Toby Fox (youtube)"), 
            ('I Thought I Saw Your Face Today', "Game\music\I Thought I Saw Your Face Today - She & Him (Instrumental)")
            ],
            onchange=music)
        
    else:
        music_selector = choice.add.selector(
            'MUSIC :', 
            [
            ('Megalovania', "Game\music\MEGALOVANIA - Toby Fox"), 
            ('Abolish the IRS', "Game\music\Abolish the IRS"), 
            ('Ana Vidovic - Asturias by Isaac Albéniz ', "Game\music\Ana Vidovic - Asturias by Isaac Albéniz -"),
            ('Like Him- Tyler the Creator', "Game\music\Like Him (Instrumental) - Tyler the Creator - pb (abandoned) (youtube)")
            ],
            onchange=music)
    choice.add.button("START GAME", start_game, music_selector)
    choice.add.button("BACK", home_screen, user, profile_options_menu)
    choice.mainloop(surface)