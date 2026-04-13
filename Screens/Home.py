import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))
fundo = pygame.image.load('./images/telainicial.png')

def home_screen(user,profile_menu):
    fundo = BaseImage(
        image_path="telainicial.png",
        drawing_mode=IMAGE_MODE_FILL
    )
    theme = pygame_menu.themes.THEME_DARK.copy()

    #Fonte e Tamanho do nome "Nord Hero"
    theme.title_font = pygame_menu.font.FONT_FRANCHISE
    theme.title_font_size = 70
    
    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior 
    theme.background_color = fundo 
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (290, 0)

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    home_menu = pygame_menu.Menu(
        f', {user[1]}',
        800,
        500,
        theme=theme
        )

    home_menu.add.label(
        f"""Name: {user[1]}
                email: {user[2]}
                password: {user[3]}
            """, font_size=30)

    home_menu.add.button("iniciar")
    home_menu.add.button("Configurações", profile_menu, user)
    home_menu.add.button("Sair do Jogo", pygame_menu.events.EXIT)
    home_menu.mainloop(surface)