import pygame
import pygame_menu


pygame.init()
surface = pygame.display.set_mode((600, 400))

def home_screen(dados):
    home_menu = pygame_menu.Menu(
        f'Bem-vindo {dados["nome"]}',
        600,
        400,
        theme=pygame_menu.themes.THEME_BLUE)

    home_menu.add.label(
        f"""Nome: {dados['nome']}, Email: {dados['email']}""", font_size=20)

    home_menu.add.button("iniciar")
    home_menu.add.button("Configurações")
    home_menu.add.button("Sair do Jogo", pygame_menu.events.EXIT)
    home_menu.mainloop(surface)