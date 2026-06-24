import pygame
import pygame_menu
from pygame_menu.baseimage import BaseImage, IMAGE_MODE_FILL

from DataBase.repositories.achievement_repository import AchievementRepository
from models.user import User

pygame.init()


def achievements_screen(user: User):
    from Screens.Home import home_screen
    from Screens.profile_options import profile_options_menu

    repository = AchievementRepository()
    all_achievements = repository.get_all()
    unlocked_keys = repository.get_unlocked_keys_by_user(user.id)
    total = len(all_achievements)
    unlocked_count = len(unlocked_keys)

    fundo = BaseImage(image_path="./Images/teladefundo.png", drawing_mode=IMAGE_MODE_FILL)
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title_font = pygame_menu.font.FONT_MUNRO
    theme.title_font_size = 20
    theme.widget_font = pygame_menu.font.FONT_MUNRO
    theme.background_color = fundo
    theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    theme.title_offset = (10, 50)
    theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()

    surface = pygame.display.get_surface()
    width, height = surface.get_size()

    menu = pygame_menu.Menu(
        f' Conquistas — {user.name}',
        width,
        height,
        theme=theme
    )

    menu.add.label(
        f"Desbloqueadas: {unlocked_count} / {total}",
        font_size=18, 
        font_name=pygame_menu.font.FONT_MUNRO, font_color=(255, 215, 0)
    )
    
    def on_selector_change(selected, value):
        if value == "desbloqueadas":
            draw_desbloqueadas()
        elif value == "bloqueadas":
            draw_bloqueadas()
            
    menu.add.selector(
        "Mostrar: ",
        [
            ("Desbloqueadas", "desbloqueadas"),
            ("Bloqueadas", "bloqueadas")
        ],
        onchange=on_selector_change
    )
          
    all_labels = []
    def clear_labels(list):
        if len(list) > 0:
            for label in all_labels:
                menu.remove_widget(label)
            all_labels.clear()
        else:
            pass
    
    all_buttons = []
    def clear_buttons(list):
        if len(list) > 0:
            for button in all_buttons:
                menu.remove_widget(button)
            all_buttons.clear()
        else:
            pass
        
    desbloqueadas = [a for a in all_achievements if a.key in unlocked_keys]
    bloqueadas = [a for a in all_achievements if a.key not in unlocked_keys]
    ITEMS_POR_PAGINA = 10
    pagina_desbloqueadas = 0
    pagina_bloqueadas = 0
    
    def prox_desbloqueadas():
        nonlocal pagina_desbloqueadas
        max_pag = (len(desbloqueadas) - 1) // ITEMS_POR_PAGINA

        if pagina_desbloqueadas < max_pag:
            pagina_desbloqueadas += 1
            draw_desbloqueadas()
            
    def ant_desbloqueadas():
        nonlocal pagina_desbloqueadas

        if pagina_desbloqueadas > 0:
            pagina_desbloqueadas -= 1
            draw_desbloqueadas()

    def prox_bloqueadas():
        nonlocal pagina_bloqueadas
        max_pag = (len(bloqueadas) - 1) // ITEMS_POR_PAGINA

        if pagina_bloqueadas < max_pag:
            pagina_bloqueadas += 1
            draw_bloqueadas()

    def ant_bloqueadas():
        nonlocal pagina_bloqueadas

        if pagina_bloqueadas > 0:
            pagina_bloqueadas -= 1
            draw_bloqueadas()
            
    def draw_desbloqueadas():
        nonlocal all_labels, all_buttons
        clear_labels(all_labels)
        clear_buttons(all_buttons)

        inicio = pagina_desbloqueadas * ITEMS_POR_PAGINA
        fim = inicio + ITEMS_POR_PAGINA         

        if desbloqueadas:
            lbl_title = menu.add.label(
                "Desbloqueadas",
                font_size=30,
                font_name=pygame_menu.font.FONT_MUNRO,
                font_color=(180, 255, 180)
            )
            all_labels.append(lbl_title)

            for achievement in desbloqueadas[inicio:fim]:
                lbl_name = menu.add.label(
                    f"{achievement.icon}  {achievement.name}",
                    font_size=25,
                    font_name=pygame_menu.font.FONT_MUNRO,
                    font_color=(220, 255, 220)
                )
                
                lbl_description = menu.add.label(
                    f"   {achievement.description}",
                    font_size=20,
                    font_name=pygame_menu.font.FONT_MUNRO,
                    font_color=(160, 200, 160)
                )
                all_labels.append(lbl_name)
                all_labels.append(lbl_description)

        if pagina_desbloqueadas > 0:
            btn_ant = menu.add.button("<-", ant_desbloqueadas)
            all_buttons.append(btn_ant)

        if fim < len(desbloqueadas):             
            btn_prox = menu.add.button("->", prox_desbloqueadas)
            all_buttons.append(btn_prox)

        voltar = menu.add.button("VOLTAR", home_screen, user, profile_options_menu)
        all_buttons.append(voltar)
        
    def draw_bloqueadas():
        nonlocal all_labels, all_buttons
        clear_labels(all_labels)
        clear_buttons(all_buttons)

        inicio = pagina_bloqueadas * ITEMS_POR_PAGINA   
        fim = inicio + ITEMS_POR_PAGINA

        if bloqueadas:
            lbl_title = menu.add.label(
                "Bloqueadas",
                font_size=30,
                font_name=pygame_menu.font.FONT_MUNRO,
                font_color=(160, 160, 160)
            )
            all_labels.append(lbl_title)

            for achievement in bloqueadas[inicio:fim]:
                lbl_name = menu.add.label(
                    f"🔒  {achievement.name}",
                    font_size=25,
                    font_name=pygame_menu.font.FONT_MUNRO,
                    font_color=(130, 130, 130)
                )
                lbl_description = menu.add.label(
                    f"{achievement.description}",
                    font_size=20,
                    font_name=pygame_menu.font.FONT_MUNRO,
                    font_color=(100, 100, 100)
                )
                all_labels.append(lbl_name)
                all_labels.append(lbl_description)

        if pagina_bloqueadas > 0:                       
            btn_ant = menu.add.button("<-", ant_bloqueadas)
            all_buttons.append(btn_ant)

        if fim < len(bloqueadas):                       
            btn_prox = menu.add.button("->", prox_bloqueadas)
            all_buttons.append(btn_prox)

        voltar = menu.add.button("VOLTAR", home_screen, user, profile_options_menu)
        all_buttons.append(voltar)
    menu.mainloop(surface)