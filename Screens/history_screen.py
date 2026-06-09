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
fundo = pygame.image.load('./Images/TelaPadrao.png')

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

    screen = pygame.display.get_surface()
    width, height = screen.get_size()
    
    history_menu = pygame_menu.Menu(
        f'',
        width,
        height,
        theme=theme
    )
    
    scoreManager = ScoreRepository()
    songManager = SongRepository()
    chartManager = SongChartsRepository()
              
    all_scores = scoreManager.get_all_by_user_id(user.id)  
    history_menu.add.label("")
    history_menu.add.label("")
    history_menu.add.label("")
    history_menu.add.label("HISTORICO DE PARTIDAS", font_size=30, font_name=pygame_menu.font.FONT_MUNRO)
    history_menu.add.label(f"TOTAL DE PARTIDAS: {len(all_scores)}", font_size=30, font_name=pygame_menu.font.FONT_MUNRO)
    history_menu.add.label("")
    
    labels = []
    selectors = []
    def clear_lists(list):
        if len(list) > 0:
            for i in list:
                history_menu.remove_widget(i)
            list.clear()
        else:
            pass
        
    def create_select_difficulty():
        selector_difficulty = history_menu.add.selector(
            "Difficulty:", 
        [
            ("---", "-"),
            ("Easy", 1),
            ("Normal", 2),
            ("Hard", 3)
        ], onchange=create_history
    )
        selectors.append(selector_difficulty)
    
    def create_select_music(charts):
        songs = [songManager.get_by_id(chart.song_id).title for chart in charts]
        songs = list(set(songs))
        music_selector = history_menu.add.selector(
         "Music: ",
         [("---", "-")] + [(song, song) for song in songs],
         onchange=create_history
        )
        selectors.append(music_selector)
        
    def create_history(selected, value):
        all_scores = scoreManager.get_all_by_user_id(user.id)  
        if value == "-":
            if selectors is not None:
                clear_lists(selectors)

            if labels is not None:
                clear_lists(labels)
            return None
           
        if value == "Geral":
            final_scores = all_scores[:]
        elif value == "Recentes":
            final_scores =  sorted(all_scores, key=lambda score: score.id, reverse=True)[:5]
        elif value == "Melhores Scores":
            final_scores = sorted(all_scores, key=lambda score: score.score, reverse=True)[:5]
            clear_lists(selectors)
        elif value == "music":
            all_charts = [chartManager.get_by_id(score.chart_id) for score in all_scores]
            clear_lists(selectors)
            create_select_music(all_charts)
            return None
        elif value == "dificuldade":
            clear_lists(labels)
            try:
                clear_lists(selectors)
            except:
                pass
            create_select_difficulty()
            return None
        elif type(value) == str:
            song = songManager.get_by_title(value)
            charts = chartManager.get_all_charts_by_song(song.id)
            print(charts)
            final_scores = []
            for chart in charts:
                score = scoreManager.get_by_user_chart_id(user.id, chart.id) 
                if len(score) > 0:
                    final_scores.extend(score)
        if type(value) == int:
            final_scores = scoreManager.get_by_user_difficulty(user.id, value)
        
        clear_lists(labels)        
        diff_map = {1: " EASY ", 2: " NORMAL ", 3: " HARD "}
       
        for score in final_scores:
            chart = chartManager.get_by_id(score.chart_id)
            song = songManager.get_by_id(chart.song_id)
            diff = diff_map.get(chart.difficulty_id, "?????")
            texto = (
                f"{song.title[:20]:<20}"
                f"{score.score:>8}"
                f"{diff:>6}"
                f"{score.accuracy:>8.1f}%"
            )   
            
            color_map = {1: (100, 255, 100), 2: (255, 255, 100), 3: (255, 100, 100)}
            color = color_map.get(chart.difficulty_id, (255, 255, 255))
            label = history_menu.add.label(
                f"{texto}",
                font_color=color,
                font_size=30,
                font_name=pygame_menu.font.FONT_MUNRO    
            )       
            
            labels.append(label)
        exit_btn =  history_menu.add.button("EXIT", home_screen, user, profile_options_menu)
        labels.append(exit_btn)
            
    choice_history = history_menu.add.selector(
        "History: ",
        [("----", "-"),
         ("Geral", "Geral"),
         ("Recentes", "Recentes"),
         ("Melhores Scores", "Melhores Scores"),
         ("Por dificuldade", "dificuldade"),
         ("Por music", "music")
        ],
        onchange=create_history
    )
    
    history_menu.add.label(
        'MUSIC                    SCORE      DIF      ACC',
        font_color=(200, 200, 200),
        font_size=35,
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    history_menu.add.label(
        '----------------------------------------------------',
        font_size=28,
        font_name=pygame_menu.font.FONT_MUNRO
    )    
    
    history_menu.add.label("")
    history_menu.mainloop(screen)