import pygame
import pygame_menu



pygame.init()
surface = pygame.display.set_mode((600, 400))

def create_account_menu(home_screen,initial_screen,login_screen):
    creat_menu = pygame_menu.Menu(
        'Bem-vindo',
        400,
        300,
        theme=pygame_menu.themes.THEME_BLUE)

    nome_input = creat_menu.add.text_input('Nome: ', default='Carlos')
    email_input = creat_menu.add.text_input('Email: ', default='Carlos@gmail.com')
    senha_input = creat_menu.add.text_input('Senha: ', password=True)

    dados = {"nome": nome_input.get_value(), "email": email_input.get_value(), "senha" : senha_input.get_value()}

    creat_menu.add.button('Criar Conta', home_screen, dados)
    creat_menu.add.button('voltar', initial_screen, login_screen,create_account_menu)
    creat_menu.mainloop(surface)
