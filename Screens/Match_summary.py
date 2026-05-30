import pygame
import pygame_menu
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from DataBase.repositories.score_repository import ScoreRepository
from DataBase.repositories.song_repository import SongRepository
from DataBase.repositories.song_chart_repository import SongChartsRepository

from Screens import choice_mod
from models.score import Score
from models.user import User

pygame.init()
screen_surface = pygame.display.set_mode((800, 500))
fundo = pygame.image.load('./Images/Summary.png')
music = ""
def match_summary(user: User, total_notes, notes_hit, file_path, score):
    """
    Exibe o resumo de desempenho após uma partida.
    
    Calcula e mostra a precisão do jogador, total de notas,
    notas acertadas e ranking (S, A, B, D) baseado na performance.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    from Screens.choice_mod import choice_mod
            
    fundo = BaseImage(
        image_path="./Images/Summary.png",
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
        f'',
        800,
        500,
        theme=theme
        )
    
    def criar_grafico_radar():
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        import numpy as np
        
        categorias = ["Miss", "Bad", "Good", "Perfect"]
        
        player1 = [notes_hit[0]["Miss"], notes_hit[0]["Bad"], notes_hit[0]["Good"], notes_hit[0]["Perfect"]]
    
        N = len(categorias)
        
        angulos = np.linspace(0 , 2*np.pi, N, endpoint=False).tolist()
        
        player1 += player1[:1]
        
        angulos += angulos[:1]
        
        fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(polar=True))
        
        ax.fill(angulos, player1, alpha=0.9)
        
        if len(notes_hit) > 1:
            player2 = [notes_hit[1]["Miss"], notes_hit[1]["Bad"], notes_hit[1]["Good"], notes_hit[1]["Perfect"]]
            player2 += player2[:1]
            ax.fill(angulos, player2, alpha=0.9)
            
            limite = max(max(player1), max(player2)) * 1.05
        else:
            limite = max(player1) * 1.05
            
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, fontsize=12, fontweight='bold', fontfamily='sans-serif', color='white')
        ax.set_ylim(0, limite)
      
        plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
        
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        ax.grid(False)
        
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        
        renderer = canvas.get_renderer()
        
        raw_data = renderer.buffer_rgba()
        
        size = canvas.get_width_height()
        
        graph_surface = pygame.image.frombuffer(raw_data, size, "RGBA")
        
        plt.close(fig)
        
        return graph_surface
                 
    def calculete_raking(user_accuracy):
        if user_accuracy >= 95 :
            return "S"  
        elif user_accuracy >= 85:
            return "A"
        elif user_accuracy >= 70:
            return "B"
        elif user_accuracy == 0:
            return "N/A"
        else:
            return "D"
        
    total_player1 = sum(notes_hit[0].values())
    
    if len(notes_hit) > 1:
        total_player2 = sum(notes_hit[1].values())
        
        hit_notes_together = total_player1 + total_player2
        accuracy = round((hit_notes_together / total_notes) * 100) if total_notes > 0 else 0   
        raking = calculete_raking(accuracy)
                                   
        mensagem_total_notes = f"Total notes: {total_notes}"
        mensagem_notes_hit = f"Hit notes together {hit_notes_together} | P1: {total_player1}  P2: {total_player2}"
        mensagem_accuracy = f"Raking: {raking},  {accuracy}% accuracy"
    else:
        accuracy = round((total_player1 / total_notes) * 100) if total_notes > 0 else 0   
        raking = calculete_raking(accuracy)
        
        mensagem_total_notes = f"Total notes: {total_notes}"
        mensagem_notes_hit = f"Hit notes: {total_player1}"
        mensagem_accuracy = f"Raking: {raking},  {accuracy}% accuracy"
    
   # 1. Criamos cada informação como um texto separado, definindo a nova fonte
    lbl_total_notes = choice.add.label(
        f"{mensagem_total_notes}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    lbl_notes_hit = choice.add.label(
        f"{mensagem_notes_hit}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    lbl_raking = choice.add.label(
        f"{mensagem_accuracy}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    scoreManager = ScoreRepository()
    songManager = SongRepository()
    chartManeger = SongChartsRepository()
    
    song = songManager.get_by_file_path(file_path)
    chart = chartManeger.get_by_song_and_difficulty(song.id, song.story_difficulty_id)
    
    score_match = Score(None, user.id, chart.id , score, accuracy, raking)
    scoreManager.create(score_match)
    
    choice.add.button("CHOOCE ANOTHER SONG", choice_mod, user)
    choice.add.button("RETURN TO HOME", home_screen, user, profile_options_menu)
    
    choice.enable()
    graph_surface = criar_grafico_radar()
    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        choice.update(events)
        choice.draw(screen_surface)
    
        screen_surface.blit(graph_surface, (10, 10))
        pygame.display.flip()