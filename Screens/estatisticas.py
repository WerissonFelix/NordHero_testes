
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from DataBase.repositories.score_repository import ScoreRepository
from models.score import Score
from models.user import User

import pygame
import pygame_menu

pygame.init()

screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()

def estatisticas_screen(user: User):   
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    
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
    
    grafico_surface = None
    def gerenciar_graficos(seleted, value):
        nonlocal grafico_surface
        if value == 'Scores':
            grafico_surface = criar_grafico_linha(value)
        elif value == 'Accuracy':
            grafico_surface = criar_grafico_linha(value)
            pass
        elif value == 'Tipos de Notas':
            grafico_surface = None
            pass
        elif value == 'Dificuldade':
            grafico_surface = None
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