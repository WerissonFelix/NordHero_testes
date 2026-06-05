import pygame
import pygame_menu

from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from models.user import User

pygame.init()
surface = pygame.display.set_mode((1080, 720))
fundo = pygame.image.load('./Images/telainicial.png')
def choice_mod(user:User):
    """
    Exibe a tela de seleção de dificuldade do jogo.
    
    Permite ao usuário escolher entre os níveis Easy, Normal e Hard,
    e navega para a tela de seleção de música com a dificuldade escolhida.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    from Screens.choice_difficulty import choice_difficulty
    
    fundo = BaseImage(
        image_path="./Images/telainicial.png",
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
        f'Connected as: {user.name}',
        1080, 
        720,
        theme=theme
        )
    
   # 1. Criamos cada informação como um texto separado, definindo a nova fonte
    lbl_nome = choice.add.label(
        f"Name: {user.name}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    
    lbl_email = choice.add.label(
        f"email: {user.email}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
  
    lbl_nome.set_float(True)
    lbl_nome.set_alignment(ALIGN_RIGHT)
    lbl_nome.translate(-20, -160)

    lbl_email.set_float(True)
    lbl_email.set_alignment(ALIGN_RIGHT)
    lbl_email.translate(-20, -135)

    lbl_nome.set_float(True)
    lbl_nome.set_alignment(ALIGN_RIGHT)
    lbl_nome.translate(-20, -160)

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
        
        continue_button = choice.add.button(
            "Continue", 
            lambda: choice_difficulty(user, "2 Players", tipo, tipo_2players)
        )
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
       
        continue_button = choice.add.button("Continue", lambda: choice_difficulty(user, "Single Player", tipo))  
        
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
                choice_difficulty(user, "2 Players", tipo, tipo_2players)
            else:
                selector_2players_type()     
        
    choice.add.label(
        "", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )

    if len(selectors) == 0 and len(buttons) == 0:
        create_mod_selector()
        
    choice.mainloop(surface)