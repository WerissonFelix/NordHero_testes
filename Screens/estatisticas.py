
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from DataBase.repositories.score_repository import ScoreRepository
from DataBase.repositories.song_chart_repository import SongChartsRepository
from DataBase.repositories.notes_hit_repository import NotesHitRepository

from models.score import Score
from models.notes_hit import NotesHit
from models.song_chart import SongChart
from models.user import User

import pygame
import pygame_menu

pygame.init()

screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()

def estatisticas_screen(user: User):   
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    import numpy as np
    
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

    estatistica_menu = pygame_menu.Menu(
        f'',
        1080,
        720,
        theme=theme
        )
    
    scoreManager = ScoreRepository()
    chartManager = SongChartsRepository()
    notesHitManager = NotesHitRepository()
    
    
    grafico_surface = None
    def gerenciar_graficos(seleted, value):
        nonlocal grafico_surface
        if value == 'Scores':
            grafico_surface = criar_grafico_linha(value)
        elif value == 'Accuracy':
            grafico_surface = criar_grafico_linha(value)
            pass
        elif value == 'Tipos de Notas':
            grafico_surface = criar_grafico_radar()
            pass
        elif value == 'Dificuldade':
            grafico_surface = criar_grafico_barra()
            pass
        else:
            grafico_surface = None
            pass
    
    type_selector = estatistica_menu.add.selector(
        "Ver grafico de: ",
        [
        ("---", '-'),
        ("Pontos/Scores", 'Scores'),
        ("Accuracy", "Accuracy"),
        ("Tipos de Notas", "Tipos de Notas"),
        ("Por Dificuldade", "Dificuldade")
        ], onchange=gerenciar_graficos
        
    )
    type_selector.translate(-20, -300)
    def criar_grafico_radar():
        nonlocal grafico_surface 
        
        notes_hit = notesHitManager.get_all()
        
        miss = [notes.qtd_miss for notes in notes_hit] if notes_hit is not None else 0
        bad = [notes.qtd_bad for notes in notes_hit] if notes_hit is not None else 0
        good = [notes.qtd_good for notes in notes_hit] if notes_hit is not None else 0
        perfect = [notes.qtd_perfect for notes in notes_hit] if notes_hit is not None else 0
        
        categorias = ["Miss", "Bad", "Good", "Perfect"]
        
        player = [sum(miss), sum(bad), sum(good), sum(perfect)]
    
        N = len(categorias)
        
        angulos = np.linspace(0 , 2*np.pi, N, endpoint=False).tolist()
        
        player += player[:1]
        
        angulos += angulos[:1]
        
        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        
        ax.fill(angulos, player, alpha=0.9)
        
        '''  
        if len(notes_hit) > 1:
            player2 = [notes_hit[1]["Miss"], notes_hit[1]["Bad"], notes_hit[1]["Good"], notes_hit[1]["Perfect"]]
            player2 += player2[:1]
            ax.fill(angulos, player2, alpha=0.9)
            
            limite = max(max(player), max(player2)) * 1.05
        else:
        '''
        
        limite = max(player) * 1.05
            
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
                 
    def criar_grafico_barra():
        all_easy = scoreManager.get_all_by_chart_difficulty(1)
        all_normal = scoreManager.get_all_by_chart_difficulty(2)
        all_hard = scoreManager.get_all_by_chart_difficulty(3)
        
        easy = [score.accuracy for score in all_easy] if all_easy is not None else 0
        normal = [score.accuracy for score in all_normal] if all_normal is not None else 0
        hard = [score.accuracy for score in all_hard] if all_hard is not None else 0 
        
        media_easy = sum(easy) // len(easy) if all_easy else 0
        media_normal = sum(normal) // len(normal) if all_normal else 0
        media_hard = sum(hard) // len(hard) if all_hard else 0
        
        dificuldades = ["Easy", "Normal", "Hard"]
        accuracies =  [media_easy, media_normal, media_hard]
        
        fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
        
        ax.barh(dificuldades, accuracies, color=['blue', 'orange', 'red'])
        
        ax.set_title("Média de Accuracy por Dificuldade", fontsize=16)
        ax.set_xlabel("Accuracy (%)", fontsize=12)
        ax.set_ylabel("Dificuldade", fontsize=12)
        
        canvas = FigureCanvasAgg(fig)
        canvas.draw()

        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()

        surface = pygame.image.frombuffer(
            raw_data,
            canvas.get_width_height(),
            "RGBA"
        )

        plt.close(fig)

        return surface
    def criar_grafico_linha(value):
        fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
        
        all_scores = scoreManager.get_all_by_user_id(user.id)
         
        scores = [score.score if value == "Scores" else score.accuracy for score in all_scores]

        ax.plot(
            range(len(scores)),
            scores,
            color='green',
            linewidth=5
        )
    
        ax.grid(True)

        title = "Evolução dos Pontos" if value == "Scores" else "Evolução da Accuracy"
        y_label = "Pontos" if value == "Scores" else "Accuracy (%)"
        
        ax.set_title(title, fontsize=16)
        ax.set_xlabel('Tentativas', fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        
        fig.tight_layout()
        
        canvas = FigureCanvasAgg(fig)
        canvas.draw()

        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()

        surface = pygame.image.frombuffer(
            raw_data,
            canvas.get_width_height(),
            "RGBA"
        )

        plt.close(fig)

        return surface
    
    back_button =estatistica_menu.add.button("BACK", home_screen, user, profile_options_menu)
    back_button.translate(-20, -300)
    estatistica_menu.enable()
    running = True
    clock = pygame.time.Clock()
    while running:
        
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                
        estatistica_menu.update(events)

        screen.fill((30, 30, 30))
        
        estatistica_menu.draw(screen)
        
        if grafico_surface is not None:
            x = (screen.get_width() - grafico_surface.get_width()) // 2

            y = (screen.get_height() - grafico_surface.get_height()) // 2 + 80

            screen.blit(grafico_surface, (x,y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()