import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

pygame.init()


def choice_verification_screen() -> str:
    """
    Exibe uma tela para o usuário escolher o método de verificação:
    envio do código por Email ou por SMS.

    Retorna:
        "email" ou "sms" conforme a escolha do usuário.
    """

    fundo = BaseImage(
        image_path="./Images/teladefundo.png",
        drawing_mode=IMAGE_MODE_FILL
    )

    theme = pygame_menu.themes.THEME_DARK.copy()

    # Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    # Cor e Estilo da Barra Superior
    theme.background_color = fundo
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (10, 50)

    # Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    escolha = {"metodo": None}

    def escolher_email():
        escolha["metodo"] = "email"
        choice_menu.disable()

    def escolher_sms():
        escolha["metodo"] = "sms"
        choice_menu.disable()

    surface = pygame.display.get_surface()
    width, height = surface.get_size()

    choice_menu = pygame_menu.Menu(
        "",
        width,
        height,
        theme=theme
    )

    choice_menu.add.label(
        "Como gostaria de receber seu codigo?",
        font_size=30,
        font_color=(255, 255, 255)
    )
    choice_menu.add.vertical_margin(20)

    choice_menu.add.button("ENVIAR POR EMAIL", escolher_email)
    choice_menu.add.button("ENVIAR POR SMS", escolher_sms)

    choice_menu.mainloop(surface)

    return escolha["metodo"]