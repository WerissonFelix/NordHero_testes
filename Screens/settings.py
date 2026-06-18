import pygame
import pygame_menu

pygame.init()
clock = pygame.time.Clock()


def change_controls_menu(config, mod):
    surface = pygame.display.get_surface()
    width, height = surface.get_size()

    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font_size = 50
    theme.widget_font_size = 28

    initial_menu = pygame_menu.Menu(
        'CONTROLES',
        width,
        height,
        theme=theme
    )

    modo_captura = False
    key_changed = None
    running = True

    keys = config.get_player_keys(mod)

    labels = {}

    status_label = initial_menu.add.label(
        "Selecione uma tecla para alterar"
    )

    initial_menu.add.vertical_margin(20)

    def update_key(key_name):
        nonlocal modo_captura, key_changed

        modo_captura = True
        key_changed = key_name

        status_label.set_title(
            f"Pressione uma tecla para {key_name.upper()}"
        )

    def refresh_labels():
        for key_name, label in labels.items():
            label.set_title(
                f"{key_name.upper()} -> {pygame.key.name(keys[key_name]).upper()}"
            )

    def change_key(new_key):
        nonlocal modo_captura, key_changed

        modo_captura = False
        keys[key_changed] = new_key

        refresh_labels()

        status_label.set_title(
            f"{key_changed.upper()} alterada para "
            f"{pygame.key.name(new_key).upper()}"
        )

    def save_config():
        nonlocal running

        config.set_player_keys(keys)

        print(keys)

        running = False

    def back():
        nonlocal running

        running = False

    # Controles
    for key_name, key_value in keys.items():

        label = initial_menu.add.label(
            f"{key_name.upper()} -> "
            f"{pygame.key.name(key_value).upper()}"
        )

        labels[key_name] = label

        initial_menu.add.button(
            f"Alterar {key_name.upper()}",
            update_key,
            key_name
        )

        initial_menu.add.vertical_margin(10)

    initial_menu.add.vertical_margin(20)

    initial_menu.add.button(
        "Confirmar",
        save_config
    )

    initial_menu.add.button(
        "Voltar",
        back
    )

    while running:

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                running = False

            if modo_captura and event.type == pygame.KEYDOWN:
                change_key(event.key)

        surface.fill((25, 25, 35))

        initial_menu.update(events)
        initial_menu.draw(surface)

        pygame.display.flip()
        clock.tick(60)