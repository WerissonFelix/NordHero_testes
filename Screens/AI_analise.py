import pygame
import pygame_menu
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from Game.GameManager.GameManager import ManageGame
from Features.AI_analytics.groq_analytics import FocusAnalyzerGroq
from models.user import User

pygame.init()
surface = pygame.display.set_mode((1080, 720))
fundo = pygame.image.load('./Images/telainicial.png')

def AI_analise(user : User):
    """
    Exibe a tela principal do jogo após o login.
    
    Mostra informações do usuário conectado e oferece opções para
    iniciar o jogo, acessar configurações ou sair do sistema.
    """
    
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu
    
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

    ai_menu = pygame_menu.Menu(
        f'Connected as: {user.name}',
        1080, 
        720,
        theme=theme
        )
    
   # 1. Criamos cada informação como um texto separado, definindo a nova fonte
    lbl_nome = ai_menu.add.label(
        f"Name: {user.name}", 
        font_size=20, 
        font_name=pygame_menu.font.FONT_MUNRO
    )
    lbl_email = ai_menu.add.label(
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
    
    def analise_rendimento_por_IA():
        analyzer = FocusAnalyzerGroq()
        resultado = analyzer.analyze_user_focus(user.id)
        if isinstance(resultado, str):
            ai_menu.add.label(
                resultado,
                wordwrap=True,
                font_size=20,
                font_name=pygame_menu.font.FONT_MUNRO
            )
            return
        focus_score = resultado["focus_score"]  
        analysis    = resultado["analysis"]

        bar_width   = 400
        bar_height  = 30
        bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)

        pygame.draw.rect(bar_surface, (60, 60, 60), (0, 0, bar_width, bar_height), border_radius=8)
       
        if focus_score >= 75:
            bar_color = (80, 200, 120)   
        elif focus_score >= 45:
            bar_color = (240, 180, 50)   
        else:
            bar_color = (220, 70, 70)   

        fill_width = int((focus_score / 100) * bar_width)
        if fill_width > 0:
            pygame.draw.rect(bar_surface, bar_color, (0, 0, fill_width, bar_height), border_radius=8)
    
        ai_menu.add.label(
            f"Nível de foco: {focus_score}/100",
            font_size=25,
            font_name=pygame_menu.font.FONT_MUNRO
        )

        ai_menu.add.surface(bar_surface)

        ai_menu.add.label(
            analysis,
            wordwrap=True,
            font_size=25,
            font_name=pygame_menu.font.FONT_MUNRO
        )

    analise_rendimento_por_IA()
    ai_menu.add.button("EXIT", home_screen, user, profile_options_menu)
    ai_menu.mainloop(surface)