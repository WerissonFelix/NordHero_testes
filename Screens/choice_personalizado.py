import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from models.user import User
from DataBase.repositories.song_repository import SongRepository
from models.difficulty import Difficulty

from Screens.Home import home_screen
from Screens.profile_options import profile_options_menu

pygame.init()

def choice_personalizado(user: User, tipo: str, mod: str = "Single Player", tipo_2players = "Contra"):
    """
    Tela que exibe todas as músicas do tipo informado.
    Para cada música, um seletor de dificuldade e um botão 'Play' na mesma linha.
    """

    fundo = BaseImage(
        image_path="./Images/teladefundo.png",
        drawing_mode=IMAGE_MODE_FILL
    )
    
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_MUNRO
    theme.title_font_size = 20
    theme.widget_font = pygame_menu.font.FONT_MUNRO
    theme.background_color = fundo
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (10, 50)
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    surface = pygame.display.get_surface()
    width, height = surface.get_size()

    menu = pygame_menu.Menu(
        f' Conectado como: {user.name}',
        width,
        height,
        theme=theme
    )

    songManager = SongRepository()

    song_list_widgets = []

    def clear_song_list():
        for widget in song_list_widgets:
            menu.remove_widget(widget)
        song_list_widgets.clear()

    def create_select_difficulty():
        menu.add.selector(
            "Difficulty:",
            [
                ("---", "-"),
                ("Easy", 1),
                ("Normal", 2),
                ("Hard", 3)
            ],
            onchange=show_songs
        )
        
    modo_jogo = 0

    def set_modo_jogo(value, selected_value):
        nonlocal modo_jogo
        modo_jogo = selected_value
        
    def show_songs(selected, value):
        nonlocal modo_jogo
        clear_song_list()

        songs = songManager.get_by_type_and_difficulty(tipo, value)
        if not songs:
            empty_label = menu.add.label("Nenhuma música encontrada para este tipo.", font_size=25)
            song_list_widgets.append(empty_label)
        else:
            row_height = 60

            for song in songs:
                # Frame com largura suficiente para acomodar todos os widgets da linha
                row = menu.add.frame_h(
                    width=int(width * 0.6),
                    height=row_height,
                    align=pygame_menu.locals.ALIGN_CENTER,
                    padding=0
                )
                row._relax = True
                song_list_widgets.append(row)

                label = menu.add.label(
                    song.title[:30] + ("..." if len(song.title) > 30 else "")
                )
                row.pack(label, align=pygame_menu.locals.ALIGN_LEFT)
                song_list_widgets.append(label)

                selector = menu.add.selector(
                    "",
                    [("Easy", 0), ("Normal", 1), ("Hard", 2)],
                    onchange=set_modo_jogo
                )
                row.pack(selector, align=pygame_menu.locals.ALIGN_LEFT)
                song_list_widgets.append(selector)

                def play_callback(song=song, selector=selector):
                    start_game_with_song(user, song, mod, modo_jogo, tipo_2players)

                play_btn = menu.add.button("Play", play_callback)
                row.pack(play_btn, align=pygame_menu.locals.ALIGN_LEFT)
                song_list_widgets.append(play_btn)

    create_select_difficulty()
    menu.add.button("VOLTAR", home_screen, user, profile_options_menu)
    menu.mainloop(surface)

def start_game_with_song(user: User, song, mod: str, difficulty, tipo_2players):
    """
    Função auxiliar para iniciar o jogo com a música e dificuldade escolhidas.
    """
    
    from Game.GameManager.GameManager import ManageGame

    if mod == "Single Player":
        game_manager = ManageGame(user, song.file_path, mod, multiplicador=difficulty)
    else:
        if tipo_2players == "Contra":
            game_manager = ManageGame(user, song.file_path, mod, difficulty, song.file_path, tipo_2players)
    game_manager.load_to_run()