import pygame
import pygame_menu
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from DataBase.repositories.score_repository import ScoreRepository
from DataBase.repositories.song_repository import SongRepository
from DataBase.repositories.song_chart_repository import SongChartsRepository
from DataBase.repositories.notes_hit_repository import NotesHitRepository
from Features.achievements_engine import AchievementsEngine
from DataBase.repositories.xp_repository import XpRepository

from models.notes_hit import NotesHit
from models.score import Score
from models.user import User

pygame.init()

fundo = pygame.image.load('./Images/SummarySingleplayer.png')
music = ""

def match_summary(user: User, total_notes, notes_hit, file_path, score, tipo_2players, title="PARTIDA FINALIZADA"):
    """
    Exibe o resumo de desempenho após uma partida.
    
    Calcula e mostra a precisão do jogador, total de notas,
    notas acertadas e ranking (S, A, B, D) baseado na performance.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    from Screens.choice_mod import choice_mod
    
    if tipo_2players == None:     
        fundo = BaseImage(
            image_path="./Images/SummarySingleplayer.png",
            drawing_mode=IMAGE_MODE_FILL
        )
        
    elif tipo_2players == "Contra":
        fundo = BaseImage(
            image_path="./Images/SummaryVersus.png",
            drawing_mode=IMAGE_MODE_FILL
        )
    else: 
        fundo = BaseImage(
            image_path="./Images/SummaryCoop.png",
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
    
    screen_surface = pygame.display.get_surface()
    width, height = screen_surface.get_size()

    choice = pygame_menu.Menu(
        '',
        width,
        height,
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
    
    lbl_title = choice.add.label( 
        title,
        font_size = 40,
        font_name=pygame_menu.font.FONT_MUNRO                             
    )
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
    notesHitManager = NotesHitRepository()
    
    song = songManager.get_by_file_path(file_path)
    chart = chartManeger.get_by_song_and_difficulty(song.id, song.story_difficulty_id)
    
    notesHitManager.create(NotesHit(None, user.id, chart.id, notes_hit[0]["Miss"], notes_hit[0]["Bad"], notes_hit[0]["Good"], notes_hit[0]["Perfect"]))
    
    notes = notesHitManager.get_by_user_chart_id(chart.id, user.id)
    
    score_match = Score(None, user.id, chart.id, notes.id, score[0], accuracy, raking)
    scoreManager.create(score_match)
    
    engine = AchievementsEngine()
    new_achievements = engine.check_all(user.id)

    if new_achievements:
        choice.add.label("", font_size=14, font_name=pygame_menu.font.FONT_MUNRO)
        choice.add.label(
            "CONQUISTA DESBLOQUEADA!",
            font_size=18,
            font_name=pygame_menu.font.FONT_MUNRO,
            font_color=(255, 215, 0)
        )
        for ach in new_achievements:
            choice.add.label(
                f"{ach.icon}  {ach.name} — {ach.description}",
                font_size=15, 
                font_name=pygame_menu.font.FONT_MUNRO,
                font_color=(220, 220, 100)
            )
            
    xp_repo   = XpRepository()
    xp_result = xp_repo.add_xp(user.id, raking, accuracy)

    choice.add.label("", font_size=14, font_name=pygame_menu.font.FONT_MUNRO)
    xp_msg = f"+ {xp_result.xp_earned} XP  →  Nível {xp_result.xp_data.level}  ({xp_result.xp_data.xp_in_level} / {xp_result.xp_data.xp_to_next_level} XP)"
    choice.add.label(
        xp_msg,
        font_size=17,
        font_name=pygame_menu.font.FONT_MUNRO,
        font_color=(100, 220, 255)
    )

    if xp_result.leveled_up:
        choice.add.label(
            f"SUBIU DE NÍVEL! Agora você é Nível {xp_result.xp_data.level}!",
            font_size=18,
            font_name=pygame_menu.font.FONT_MUNRO,
            font_color=(255, 215, 0)
        )      
        
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