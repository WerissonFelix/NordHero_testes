import pygame
import pygame_menu

from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from DataBase.repositories.score_repository import ScoreRepository
from DataBase.repositories.song_chart_repository import SongChartsRepository
from DataBase.repositories.song_repository import SongRepository

from models.score import Score
from models.user import User

pygame.init()
surface = pygame.display.set_mode((800, 500))
fundo = pygame.image.load('./Images/telainicial.png')

def history_screen(user : User):
    """
    Exibe a tela principal do jogo após o login.
    
    Mostra informações do usuário conectado e oferece opções para
    iniciar o jogo, acessar configurações ou sair do sistema.
    """
    
    from Screens.choice_mod import choice_mod
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

    history_menu = pygame_menu.Menu(
        f'Connected as: {user.name}',
        800,
        500,
        theme=theme
    )
    
    scoreManager = ScoreRepository()
    songManager = SongRepository()
    chartManager = SongChartsRepository()
    
    history_menu.add.vertical_margin(80)
    table = history_menu.add.table()
    
    all_scores = scoreManager.get_all_by_user_id(user.id)
    table.add_row(
        ["Song", "Score", "Difficulty", "Accuracy"],
        cell_align=pygame_menu.locals.ALIGN_CENTER
    )
    # 1. Criamos cada informação como um texto separado, definindo a nova fonte
    for score in all_scores:
        chart = chartManager.get_by_id(score.chart_id)
        song = songManager.get_by_id(chart.song_id)
        
        table.add_row([f"{song.title} ", f"{score.score}", f"{chart.difficulty_id} ", f"{score.accuracy}%"])
    
    table.set_float(True)
    table.translate(0, 50)
    
    lbl_email = history_menu.add.label(
        f"email: {user.email}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    lbl_email.set_float(True)
    lbl_email.set_alignment(ALIGN_RIGHT)
    lbl_email.translate(-20, -135)

    history_menu.add.button("EXIT", home_screen, user, profile_options_menu)
    history_menu.mainloop(surface)