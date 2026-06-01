
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
    
    def criar_grafico():
        scoreManager = ScoreRepository()
        
        all_scores = scoreManager.get_all_by_user_id(user.id)
        
        scores = [score.score for score in all_scores]

        fig, ax = plt.subplots(figsize=(5, 5), dpi=100)

        ax.plot(
            range(len(scores)),
            scores,
            color='green',
            linewidth=5
        )
    
        ax.grid(True)

        ax.set_title('Evolução dos Pontos', fontsize=16)
        ax.set_xlabel('Tentativas', fontsize=12)
        ax.set_ylabel('Pontos', fontsize=12)
        
        
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

    grafico_surface = criar_grafico()

    running = True
    clock = pygame.time.Clock()
    x = (screen.get_width() - grafico_surface.get_width()) // 2
    y = 150
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))
        
        estatistica_menu.draw(screen)
        
        screen.blit(grafico_surface, (x,y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()