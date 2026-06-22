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
    
    menu.add.label("", font_size=10, font_name=pygame_menu.font.FONT_MUNRO)

    desbloqueadas = [a for a in all_achievements if a.key in unlocked_keys]
    bloqueadas = [a for a in all_achievements if a.key not in unlocked_keys]

    if desbloqueadas:
        menu.add.label("── Desbloqueadas ──", font_size=16, font_name=pygame_menu.font.FONT_MUNRO, font_color=(180, 255, 180))
        for ach in desbloqueadas:
            menu.add.label(f"{ach.icon}  {ach.name}", font_size=16, font_name=pygame_menu.font.FONT_MUNRO, font_color=(220, 255, 220))
            menu.add.label(f"   {ach.description}", font_size=13, font_name=pygame_menu.font.FONT_MUNRO, font_color=(160, 200, 160))

    if bloqueadas:
        menu.add.label("", font_size=10, font_name=pygame_menu.font.FONT_MUNRO)
        menu.add.label("── Bloqueadas ──", font_size=16, font_name=pygame_menu.font.FONT_MUNRO, font_color=(160, 160, 160))
        for ach in bloqueadas:
            menu.add.label(f"🔒  {ach.name}", font_size=16, font_name=pygame_menu.font.FONT_MUNRO, font_color=(130, 130, 130))
            menu.add.label(f"   {ach.description}", font_size=13, font_name=pygame_menu.font.FONT_MUNRO, font_color=(100, 100, 100))

    menu.add.label("", font_size=10, font_name=pygame_menu.font.FONT_MUNRO)
    menu.add.button("VOLTAR", home_screen, user, profile_options_menu)
    menu.mainloop(surface)