import pygame
import pygame_menu
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL
from Game.GameManager.GameManager import ManageGame

pygame.init()
surface = pygame.display.set_mode((800, 500))
fundo = pygame.image.load('./Images/telainicial.png')
music = ""
def choice_music(user):
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
    lbl_senha = choice.add.label(
        f"password: {user[3]}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    lbl_nome.set_float(True)
    lbl_nome.set_alignment(ALIGN_RIGHT)
    lbl_nome.translate(-20, -160)

    lbl_email.set_float(True)
    lbl_email.set_alignment(ALIGN_RIGHT)
    lbl_email.translate(-20, -135)

    lbl_senha.set_float(True)
    lbl_senha.set_alignment(ALIGN_RIGHT)
    lbl_senha.translate(-20, -110)
  
    lbl_nome.set_float(True)
    lbl_nome.set_alignment(ALIGN_RIGHT)
    lbl_nome.translate(-20, -160)
    
    selected_music = [None]
    
    def set_music_path(selected_item, value):
        selected_music[0] = value
        print(f"Música selecionada: {value}") 
    
    music_selector = choice.add.selector(
        'MUSIC :', 
        [('abolish the IRS', "Game\music\Abolish the IRS"), 
        ('I Thought I Saw Your Face Today', "Game\music\I Thought I Saw Your Face Today - She & Him (Instrumental)")],
        onchange=music)
    
    def start_game():
        if selected_music[0] is None:
            selected_music[0] = music_selector.get_value()[0][1]
        
        gameManager = ManageGame(user,selected_music[0])
        gameManager.load_to_run()
        
    choice.add.button("START GAME", start_game)
    choice.add.button("BACK", home_screen, user, profile_options_menu)
    choice.mainloop(surface)