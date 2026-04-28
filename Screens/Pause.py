import pygame
import pygame_menu

from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

pygame.init()
surface = pygame.display.set_mode((800, 500))

def pause_menu(user,music_path, total_notes, notes_hit):
    """
    Exibe o menu de pausa durante o jogo.
    
    Oferece opções para retomar o jogo, acessar configurações
    ou sair da partida atual mostrando o resumo do jogo.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    from Screens.Match_summary import match_summary
    from Game.GameManager.GameManager import ManageGame
    
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_BEBAS
    
    fundo_update_menu = BaseImage(
        image_path="./Images/TelaUpdateScreen.png",
        drawing_mode=IMAGE_MODE_FILL
    )

    theme.background_color = fundo_update_menu

    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior
    theme.title_background_color = (0, 0, 0)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (350, 0)

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
    
    menu = pygame_menu.Menu(
        '',
        800,
        500,

        theme=theme)
    
    manager = ManageGame(user,music_path)
    
    def resume_game():
        menu.disable()
         
    menu.add.button("SETTINGS",)
    menu.add.button('RESUME', resume_game)
    menu.add.button("QUIT", match_summary, user, total_notes, notes_hit)

    menu.mainloop(surface)