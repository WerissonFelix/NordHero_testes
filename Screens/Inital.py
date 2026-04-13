import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((800, 500))

def initial_screen(login_screen,create_account_menu):
    theme = pygame_menu.themes.THEME_DARK.copy()
    #Fonte e Tamanho do nome "Nord Hero"
    theme.title_font = pygame_menu.font.FONT_FRANCHISE
    theme.title_font_size = 70
    
    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior
    theme.title_background_color = (75, 0, 130)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
    theme.title_offset = (290, 0)

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    initial_menu = pygame_menu.Menu(
        'Nord Hero',
        800,
        500,
        theme=theme )

    initial_menu.add.button('Login', login_screen,initial_screen)
    initial_menu.add.button('Criar Conta', create_account_menu,initial_screen, login_screen)
    initial_menu.add.button('Sair', pygame_menu.events.EXIT)

    initial_menu.mainloop(surface)
