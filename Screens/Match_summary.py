import pygame
import pygame_menu
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

pygame.init()
surface = pygame.display.set_mode((800, 500))
fundo = pygame.image.load('./Images/Summary.png')
music = ""
def match_summary(user, total_notes, notes_hit):
    """
    Exibe o resumo de desempenho após uma partida.
    
    Calcula e mostra a precisão do jogador, total de notas,
    notas acertadas e ranking (S, A, B, D) baseado na performance.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    from Screens.choice_difficulty import choice_difficulty
    
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
        f'Connected as: {user[1]}',
        800,
        500,
        theme=theme
        )
    
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
    
    accuracy = round((notes_hit / total_notes) * 100) if total_notes > 0 else 0    
    
   # 1. Criamos cada informação como um texto separado, definindo a nova fonte
    lbl_total_notes = choice.add.label(
        f"Total notes: {total_notes}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    lbl_notes_hit = choice.add.label(
        f"Hit notes: {notes_hit}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    raking = calculete_raking(accuracy)
    
    lbl_raking = choice.add.label(
        f"Raking: {raking},  {accuracy}% accuracy", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    choice.add.button("CHOOCE ANOTHER SONG", choice_difficulty, user)
    choice.add.button("RETURN TO HOME", home_screen, user, profile_options_menu)
    choice.mainloop(surface)