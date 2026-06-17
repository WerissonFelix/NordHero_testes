import pygame
import pygame_menu

from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from Game.GameManager.GameManager import ManageGame
from DataBase.repositories.song_chart_repository import SongChartsRepository
from DataBase.repositories.song_repository import SongRepository
from DataBase.repositories.multiplayer_songs_repository import MultiplayerSongsRepository
from DataBase.repositories.score_repository import ScoreRepository

from models.difficulty import Difficulty
from models.user import User

pygame.init()
fundo = pygame.image.load('./Images/teladefundo.png')
music = None
def choice_music(user: User, difficulty: Difficulty, mod:str, tipo:str, tipo_2players = None):
    """
    Exibe a tela de seleção de música baseada na dificuldade escolhida.
    
    Apresenta diferentes listas de músicas conforme o nível de dificuldade
    e permite iniciar o jogo com a música selecionada.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    
    fundo = BaseImage(
        image_path="./Images/teladefundo.png",
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
    
    surface = pygame.display.get_surface()
    width, height = surface.get_size()

    choice = pygame_menu.Menu(
        f' Connected as: {user.name}',
        width,
        height,
        theme=theme
    )
    
    lbl_rank_personal = choice.add.label(
        f"Best Score: 'N/A'", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
      
    selected_music = [None] 
    
    def start_game(music_selector):
        if selected_music[0] is None:
            selected_music[0] = music_selector.get_value()[0][1][0]

        if mod == "2 Players":
            if tipo_2players == "Contra":
                gameManager = ManageGame(user, selected_music[0], mod, selected_music[0], tipo_2players)    
            else:    
                multi_song = multiSongManeger.get_by_id(music_selector.get_value()[0][1][1])
                instrumental_song = songManeger.get_by_id(multi_song.instrumental_song)
                vocal_song = songManeger.get_by_id(multi_song.vocal_song)
                
                gameManager = ManageGame(user, instrumental_song.file_path, mod, vocal_song.file_path, tipo_2players)
        else:
            print(mod)
            gameManager = ManageGame(user, selected_music[0], mod)
            
        gameManager.load_to_run()
    
    chartManeger = SongChartsRepository()
    songManeger = SongRepository()
    scoreManeger = ScoreRepository()
    multiSongManeger = MultiplayerSongsRepository()
    
    table = choice.add.table()
    def change_rank(selected, value):
        global music
        file_path, song_id = value
        music = file_path
        
        chart = chartManeger.get_by_song_and_difficulty(song_id, difficulty.id)
        score = scoreManeger.get_best_by_user_and_chart(user.id, chart.id)
        
        print(score)
        
        lbl_rank_personal.set_title(
            f"""Best Score: {score.rank if score else 'N/A'} | Best Accuracy: {score.accuracy if score else 'N/A'}%"""
        )
        
        scores = scoreManeger.get_top_scores_by_chart(chart.id)
        
        try: 
            table.clear()          
        except AssertionError as e:   
            pass
        if scores is not None:
            for score in scores:
                table.add_row([f"Score: {score.score}", f"Rank: {score.rank}", f"Accuracy: {score.accuracy}%"])  
                                
        table.cell_border_color = (255, 255, 255)
    
    if mod == "2 Players":
        if tipo_2players == "Contra":
            songs = songManeger.get_by_type_and_difficulty(tipo, difficulty.id)    
            music_selector = choice.add.selector(
                'MUSIC :',
                [(song.title[:30] + " ... ", (song.file_path, song.id)) for song in songs],
                onchange=change_rank           
            )  
        else:
            songs = multiSongManeger.get_by_difficulty(difficulty.id)
            music_selector = choice.add.selector(
                'MUSIC :',
                [(song.title[:30] + " ... ", (song.file_path, song.id)) for song in songs ],
            )
        
    else:
        print(mod)
        songs = songManeger.get_by_type_and_difficulty(tipo, difficulty.id)    
        music_selector = choice.add.selector(
            'MUSIC :',
            [(song.title[:30] + " ... ", (song.file_path, song.id)) for song in songs],
            onchange=change_rank           
        )
    
    choice.add.button("START GAME", start_game, music_selector)
    choice.add.button("BACK", home_screen, user, profile_options_menu)
    choice.mainloop(surface)