import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))

def update_menu(user, profile_options):
    from Features.Dados_Verificacao import DataVerifier
    update = pygame_menu.Menu(
        'Atualizar dados',
        800,
        500,

        theme=pygame_menu.themes.THEME_DARK)

    update.add.label(f"Nome: {user[1]}   email: {user[2]}")

    validator = DataVerifier("update_screen")

    nome_input = update.add.text_input('Nome: ', default=user[1])

    email_input = update.add.text_input('Email: ', default=user[2])

    update.add.button("Atualizar", validator.verify_just_for_update, email_input, nome_input, user[0])
    update.add.button('Voltar', profile_options, user)

    update.mainloop(surface)
