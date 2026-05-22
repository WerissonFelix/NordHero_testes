import pygame
import pygame_menu

from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from Game.GameManager.GameManager import ManageGame
from DataBase.repositories.song_chart_repository import SongChartsRepository
from DataBase.repositories.song_repository import SongRepository
from DataBase.repositories.score_repository import ScoreRepository

from models.difficulty import Difficulty
from models.user import User

pygame.init()
surface = pygame.display.set_mode((800, 500))
fundo = pygame.image.load('./Images/telainicial.png')
music = None
def choice_music(user: User, difficulty: Difficulty):
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
    
    lbl_rank_personal = choice.add.label(
        f"Best Score: 'N/A'", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    lbl_rank_global = choice.add.label(
        f"Best Scores: 'N/A'", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    selected_music = [None] 
    
    def start_game(music_selector):
        if selected_music[0] is None:
            selected_music[0] = music_selector.get_value()[0][1][0]
        
        gameManager = ManageGame(user,selected_music[0])
        gameManager.load_to_run()
    
    chartManeger = SongChartsRepository()
    songManeger = SongRepository()
    scoreManeger = ScoreRepository()
    
    all_charts = chartManeger.get_all_charts_by_difficulty(difficulty.id)
    
    songs = songManeger.get_by_story_difficulty_id(difficulty.id)
    
    def change_rank(selected, value):
        global music
        file_path, song_id = value
        music = file_path
        
        chart = chartManeger.get_by_song_and_difficulty(song_id, difficulty.id)
        score = scoreManeger.get_best_by_user_and_chart(user.id, chart.id)
        
        print(score)
        
        lbl_rank_personal.set_title(
            f"""Best Score: {score.rank if score else 'N/A'}
                Best Accuracy: {score.accuracy if score else 'N/A'}%
            """
        )
        
        scores = scoreManeger.get_top_scores_by_chart(chart.id)
        
        if scores is None:
            ranks = None
        else:
            ranks = ", ".join(s.rank if s is not None else "N/A" for s in scores)  
         
        lbl_rank_global.set_title(
            f"""Best Scores: {ranks if ranks else 'N/A'}
            """
        )
        
    music_selector = choice.add.selector(
        'MUSIC :',
        [(song.title, (song.file_path, song.id)) for song in songs],
        onchange=change_rank           
    )

    choice.add.button("START GAME", start_game, music_selector)
    choice.add.button("BACK", home_screen, user, profile_options_menu)
    choice.mainloop(surface)