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
        f'',
        800,
        500,
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
    
    def create_history(selected, value):
        all_scores = scoreManager.get_all_by_user_id(user.id)    
        if value == "Recentes":
            final_scores =  sorted(all_scores, key=lambda score: score.id, reverse=True)[:5]
        elif value == "Melhores Scores":
            final_scores = sorted(all_scores, key=lambda score: score.score, reverse=True)[:5]
        elif value == "Melhores Scores":
            print(value)
        elif value == "music":
            print(value)
        elif value == "dificuldade":
            print(value)
        else:
            final_scores = all_scores[:]
        
        if len(labels) > 0:
            print(labels)
            for label in labels:
                history_menu.remove_widget(label)
            labels.clear()
        else:
            pass
            
        for score in final_scores:
            chart = chartManager.get_by_id(score.chart_id)
            song = songManager.get_by_id(chart.song_id)
            
            texto = (
                f"{song.title[:20]:<20}"
                f"{score.score:>8}"
                f"{chart.difficulty_id:>6}"
                f"{score.accuracy:>8.1f}%"
            )   
            
            label = history_menu.add.label(
                f"{texto}",
                font_size=30,
                font_name=pygame_menu.font.FONT_MUNRO    
            )       
            
            labels.append(label)
            
    choice_history = history_menu.add.selector(
        "History: ",
        [("Geral", "Geral"),
         ("Recentes", "Recentes"),
         ("Melhores Scores", "Melhores Scores"),
         ("Por music", "music"),
         ("Por dificuldade", "dificuldade")  
        ],
        onchange=create_history
    )
    
    history_menu.add.label(
        'MÚSICA                    SCORE      DIF      ACC',
        font_size=30,
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    history_menu.add.label(
        '----------------------------------------------------',
        font_size=28,
        font_name=pygame_menu.font.FONT_MUNRO
    )    
    history_menu.add.label("")
    
    history_menu.add.button("EXIT", home_screen, user, profile_options_menu)
    history_menu.mainloop(surface)