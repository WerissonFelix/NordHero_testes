import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from Screens.Home import home_screen
from DataBase.deletes import delete_user
from DataBase.repositories.user_repository import UserRepository
from models.user import User

pygame.init()
surface = pygame.display.set_mode((600, 400))

def delete_menu(user, profile_options):
    """
    Exibe a tela de confirmação para exclusão de conta.
    
    Pergunta ao usuário se deseja realmente deletar sua conta
    e executa a exclusão permanente dos dados se confirmado.
    """
    from Screens.Inital import initial_screen
    from Screens.Logon import login_screen
    from Screens.Creat_Account import create_account_menu
    
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_BEBAS
    
    fundo_delete_menu = BaseImage(
        image_path="./Images/TelaDeleteAccount.png",
        drawing_mode=IMAGE_MODE_FILL
    )

    theme.background_color = fundo_delete_menu

    #Fonte dos Botões
    theme.widget_font = pygame_menu.font.FONT_MUNRO

    #Cor e Estilo da Barra Superior
    theme.title_background_color = (0, 0, 0)
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (350, 0)

    #Estilo de Seleção de Item
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    delete  = pygame_menu.Menu(
        '',
        800,
        500,

        theme=theme)
    
    userr = User(user[0],user[1], user[2], user[3])
    userRepository = UserRepository()
    
    delete.add.label(f"DO YOU WANT TO DELETE YOUR ACCOUNT?", font_color=(255, 255, 0))

    def deletar():
        userRepository.delete(userr.id)
        return initial_screen(login_screen,create_account_menu)
    
    delete.add.button("DELETE", deletar)
    delete.add.button('BACK', profile_options, user)

    delete.mainloop(surface)
