import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

pygame.init()
surface = pygame.display.set_mode((600, 400))

def update_menu(user, profile_options):
    from Features.Dados_Verificacao import DataVerifier
    
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
    
    update = pygame_menu.Menu(
        '',
        800,
        500,

        theme=theme)

    update.add.label(f"Name: {user[1]}   Email: {user[2]}", font_color=(255, 255, 0))
    
    validator = DataVerifier("update_screen")

    nome_input = update.add.text_input('Name: ', default=user[1])
    nome_input.set_alignment(pygame_menu.locals.ALIGN_LEFT)
    nome_input.translate(180, 0)

    email_input = update.add.text_input('Email: ', default=user[2])
    email_input.set_alignment(pygame_menu.locals.ALIGN_LEFT)
    email_input.translate(180, 0)

    update.add.button("UPDATE", validator.verify_just_for_update, email_input, nome_input, user[0])
    update.add.button('BACK', profile_options, user)

    update.mainloop(surface)
