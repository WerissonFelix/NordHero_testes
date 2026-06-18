import pygame
import pygame_menu

from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from models.user import User

pygame.init()
fundo = pygame.image.load('./Images/teladefundo.png')
def choice_mod(user:User):
    """
    Exibe a tela de seleção de dificuldade do jogo.
    
    Permite ao usuário escolher entre os níveis Easy, Normal e Hard,
    e navega para a tela de seleção de música com a dificuldade escolhida.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    from Screens.choice_difficulty import choice_difficulty
    from Screens.choice_personalizado import choice_personalizado
    
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
     
    selectors = []
    buttons = []
    def clear_lists():
        nonlocal selectors, buttons
        if len(selectors) > 0:
            for i in selectors:
                choice.remove_widget(i)
            selectors.clear()
            
        if len(buttons) > 0:
            for i in buttons:
                choice.remove_widget(i)
            buttons.clear()    
        
    mod = "Single Player"
    def set_mod(value, selected_value):
        nonlocal  mod
        mod = selected_value
        print(mod)
    
    tipo = "Instrumental"
    def set_type(value, selected_value):
        nonlocal tipo 
        tipo = selected_value
        return tipo
    
    tipo_2players = "-"
    def set_tipo_2players(value, selected_value):
        nonlocal tipo_2players
        tipo_2players = selected_value
    
    modo_jogo = "History"

    def set_modo_jogo(value, selected_value):
        nonlocal modo_jogo
        modo_jogo = selected_value
        
    def create_mod_selector():  
        clear_lists()
              
        mod_selector = choice.add.selector(
        "Select Mod :", 
        [
            ("Single Player", "Single Player"),
            ("2 Players", "2 Players")
        ],
        onchange=set_mod
        )

        selectors.append(mod_selector)
        
        continue_button = choice.add.button("Continue", selectors_manager)
        exit_button = choice.add.button("BACK", home_screen, user, profile_options_menu) 
        buttons.append(continue_button)       
        buttons.append(exit_button)
    
    def selector_2players_type():
        clear_lists()
        
        selector_2players_type = choice.add.selector(
                'Type: ',
                [   
                    ("---", "-"),
                    ("Contra", "Contra"),
                    ("Juntos", "Juntos")
                ], onchange=set_tipo_2players
            )
            
        selectors.append(selector_2players_type)
        
        continue_button = choice.add.button("Continue", selectors_manager)
        exit_button = choice.add.button("BACK", create_mod_selector)        
        buttons.append(continue_button)
        buttons.append(exit_button)        
    
    def select_vocal_instrumental_2p(tipo_2players):
        nonlocal tipo
        
        clear_lists()
        
        selector = choice.add.selector(
            'Type: ',
            [("Instrumental", "Instrumental"), ("Vocal", "Vocal")]
            , onchange=set_type
        )
        selectors.append(selector)
        
        continue_button = choice.add.button("Continue", select_history_or_custom)
        exit_button = choice.add.button("BACK", selector_2players_type)
        buttons.append(continue_button)
        buttons.append(exit_button)
        
    def select_vocal_instrumental_1p():
        clear_lists()
        
        selector_type = choice.add.selector(
            'Type: ',
            [
                ("Instrumental", "Instrumental"),
                ("Vocal", "Vocal")
            ], onchange=set_type
        )
        
        selectors.append(selector_type)
       
        continue_button = choice.add.button("Continue", select_history_or_custom)  
        
        exit_button = choice.add.button("BACK", create_mod_selector)        
        buttons.append(continue_button)
        buttons.append(exit_button)        
    
    def selectors_manager():
        nonlocal mod, tipo_2players
        
        if mod == "Single Player":
            select_vocal_instrumental_1p()
        else:
            if tipo_2players == "Contra":
                select_vocal_instrumental_2p(tipo_2players)
            elif tipo_2players == "Juntos":
                choice_difficulty(user, mod, tipo, tipo_2players)
            else:
                selector_2players_type()     
        
    choice.add.label(
        "", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )

    def select_history_or_custom():
        clear_lists()

        selector = choice.add.selector(
            "Mode: ",
            [
                ("History", "History"),
                ("Personalizado", "Personalizado")
            ],
            onchange=set_modo_jogo
        )

        selectors.append(selector)

        continue_button = choice.add.button(
            "Continue",
            final_destination
        )

        exit_button = choice.add.button(
            "BACK",
            create_mod_selector  
        )

        buttons.append(continue_button)
        buttons.append(exit_button)
    
    def final_destination():
        nonlocal mod, tipo_2players, tipo
        
        if modo_jogo == "History":
            if mod == "Single Player":
                choice_difficulty(user, mod, tipo)
            else:
                print(f"modd {mod} tipoo {tipo} tipo2 {tipo_2players}")
                choice_difficulty(user, mod, tipo, tipo_2players)
           
        else:
            choice_personalizado(user, tipo, mod)
             
    if len(selectors) == 0 and len(buttons) == 0:
        create_mod_selector()
        
    choice.mainloop(surface)