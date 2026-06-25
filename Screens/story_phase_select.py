import pygame
from DataBase.repositories.song_repository import SongRepository
from DataBase.repositories.xp_repository import XpRepository
from DataBase.repositories.story_repository import StoryRepository

from models.difficulty import Difficulty
from models.phase import Phase
from models.user import User

pygame.init()

COLORS = {1:(0, 200, 80), 2:(220, 200, 0), 3:(180, 30, 30),}

CARD_W, CARD_H = 130, 130
CARD_RADIUS = 18
CARD_BORDER = 4
CARDS_PER_ROW = 6
CARD_GAP = 20

def _draw_phase_cards(surface, phases, color, selected_index, offset_y):
    total_w = CARDS_PER_ROW * CARD_W + (CARDS_PER_ROW - 1) * CARD_GAP
    start_x = (surface.get_width() - total_w) // 2
    lock_font = pygame.font.SysFont("segoeui", 48)
    num_font  = pygame.font.SysFont("arial", 42, bold=True)

    for i, phase in enumerate(phases):
        col = i % CARDS_PER_ROW
        row = i // CARDS_PER_ROW
        x = start_x + col * (CARD_W + CARD_GAP)
        y = offset_y + row * (CARD_H + CARD_GAP)
        rect = pygame.Rect(x, y, CARD_W, CARD_H)

        bg_color = (20, 20, 20) if phase.unlocked else (10, 10, 10)
        pygame.draw.rect(surface, bg_color, rect, border_radius=CARD_RADIUS)

        border_w = CARD_BORDER + 2 if i == selected_index else CARD_BORDER
        pygame.draw.rect(surface, color, rect, width=border_w, border_radius=CARD_RADIUS)

        if phase.unlocked:
            num_text = num_font.render(f"{phase.number:02d}", True, (255, 255, 255))
            surface.blit(num_text, num_text.get_rect(center=rect.center))
        else:
            lock_text = lock_font.render("🔒", True, (120, 120, 120))
            surface.blit(lock_text, lock_text.get_rect(center=rect.center))

def story_phase_select(user: User, difficulty: Difficulty, mod: str, tipo: str, tipo_2players=None):
    from Screens.choice_difficulty import choice_difficulty

    songManager = SongRepository()
    xpManager = XpRepository()
    storyManager = StoryRepository()

    songs = songManager.get_by_type_and_difficulty(tipo, difficulty.id)
    completed = storyManager.get_completed_phases(user.id, difficulty.id, tipo)
    max_unlocked = storyManager.get_max_unlocked_phase(user.id, difficulty.id, tipo)
    xp_data = xpManager.get_user_xp(user.id)

    phases = []
    for i, song in enumerate(songs, start=1):
        phases.append(Phase(number = i, unlocked= i <= max_unlocked, song= song, done = i in completed ))

    color = COLORS.get(difficulty.id, (255, 255, 255))
    surface = pygame.display.get_surface()
    width, height = surface.get_size()

    try:
        background = pygame.image.load("./Images/teladefundo.png").convert()
        background = pygame.transform.scale(background, (width, height))
    except Exception:
        background = None

    font_title = pygame.font.SysFont("arial", 26, bold=True)
    font_label = pygame.font.SysFont("arial", 18)
    font_song = pygame.font.SysFont("arial", 16)
    font_btn = pygame.font.SysFont("arial", 22, bold=True)
    font_xp = pygame.font.SysFont("arial", 16)
    font_level = pygame.font.SysFont("arial", 14, bold=True)

    diff_names = {1: "FÁCIL", 2: "NORMAL", 3: "DIFÍCIL"}
    diff_label = diff_names.get(difficulty.id, "")

    selected_idx = 0
    CARDS_TOP = 220
    clock = pygame.time.Clock()

    def btn_rect(label, cx, cy):
        w, h = font_btn.size(label)
        return pygame.Rect(cx - w // 2 - 10, cy - h // 2 - 6, w + 20, h + 12)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_idx = selected_idx - 1
                    while new_idx >= 0 and not phases[new_idx].unlocked:
                        new_idx -= 1
                    if new_idx >= 0:
                        selected_idx = new_idx

                elif event.key == pygame.K_RIGHT:
                    new_idx = selected_idx + 1
                    while new_idx < len(phases) and not phases[new_idx].unlocked:
                        new_idx += 1
                    if new_idx < len(phases):
                        selected_idx = new_idx

                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    phase = phases[selected_idx]
                    if phase.unlocked:
                        _start_phase(user, phase, difficulty, mod, tipo, tipo_2players, storyManager)
                        completed = storyManager.get_completed_phases(user.id, difficulty.id, tipo)
                        max_unlocked = storyManager.get_max_unlocked_phase(user.id, difficulty.id, tipo)
                        xp_data  = xpManager.get_user_xp(user.id)
                        for j, phase in enumerate(phases):
                            phase.unlocked = (j + 1) <= max_unlocked
                            phase.done = (j + 1) in completed

                elif event.key == pygame.K_ESCAPE:
                    choice_difficulty(user, mod, tipo, tipo_2players)
                    return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                total_w = CARDS_PER_ROW * CARD_W + (CARDS_PER_ROW - 1) * CARD_GAP
                start_x = (surface.get_width() - total_w) // 2
                for i, phase in enumerate(phases):
                    col = i % CARDS_PER_ROW
                    row = i // CARDS_PER_ROW
                    x = start_x + col * (CARD_W + CARD_GAP)
                    y = CARDS_TOP + row * (CARD_H + CARD_GAP)
                    if pygame.Rect(x, y, CARD_W, CARD_H).collidepoint(mx, my):
                        if phase.unlocked:
                            selected_idx = i
                            _start_phase(user, phase, difficulty, mod, tipo, tipo_2players, storyManager)
                            completed = storyManager.get_completed_phases(user.id, difficulty.id, tipo)
                            max_unlocked = storyManager.get_max_unlocked_phase(user.id, difficulty.id, tipo)
                            xp_data = xpManager.get_user_xp(user.id)
                            for j, phase in enumerate(phases):
                                phase.unlocked = (j + 1) <= max_unlocked
                                phase.done = (j + 1) in completed

                if btn_rect("VOLTAR", width // 2 - 80, height - 80).collidepoint(mx, my):
                    choice_difficulty(user, mod, tipo, tipo_2players)
                    return
        
        if background:
            surface.blit(background, (0, 0))
        else:
            surface.fill((0, 0, 0))

        _draw_xp_card(surface, user, xp_data, color, font_level, font_xp)

        title_surf = font_title.render(f"MODO HISTÓRIA — {diff_label}", True, color)
        surface.blit(title_surf, (width // 2 - title_surf.get_width() // 2, 150))

        _draw_phase_cards(surface, phases, color, selected_idx, CARDS_TOP)

        phase = phases[selected_idx]
        if phase.unlocked and phase.song:
            song_name = phase.song.title[:55] + ("…" if len(phase.song.title) > 55 else "")
            song_surf = font_song.render(song_name, True, (200, 200, 200))
            surface.blit(song_surf, (width // 2 - song_surf.get_width() // 2, CARDS_TOP + CARD_H + 30))
            done_text  = "✓ Completa" if phase.done else "— Não jogada ainda"
            done_color = (100, 255, 100) if phase.done else (180, 180, 180)
            done_surf  = font_label.render(done_text, True, done_color)
            surface.blit(done_surf, (width // 2 - done_surf.get_width() // 2, CARDS_TOP + CARD_H + 55))

        _draw_btn(surface, "VOLTAR", width // 2 - 80, height - 80, color, font_btn)

        hint = font_xp.render("← → para navegar   ENTER para jogar   ESC para voltar", True, (120, 120, 120))
        surface.blit(hint, (width // 2 - hint.get_width() // 2, height - 40))

        pygame.display.flip()
        clock.tick(60)
        
def _draw_xp_card(surface, user, xp_data, color, font_level, font_xp):
    card_rect = pygame.Rect(10, 10, 260, 80)
    pygame.draw.rect(surface, (20, 20, 20), card_rect, border_radius=10)
    pygame.draw.rect(surface, color, card_rect, width=2, border_radius=10)
    pygame.draw.circle(surface, (50, 50, 50), (55, 50), 30)
    pygame.draw.circle(surface, color, (55, 50), 30, width=2)

    name_surf = font_level.render(user.name[:18], True, (255, 255, 255))
    surface.blit(name_surf, (95, 18))
    lvl_surf = font_level.render(f"Nível {xp_data.level}", True, color)
    surface.blit(lvl_surf, (200, 18))

    bar_x, bar_y, bar_w, bar_h = 95, 42, 155, 12
    pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
    progress = xp_data.xp_in_level / xp_data.xp_to_next_level
    fill_w = int(bar_w * progress)
    if fill_w > 0:
        pygame.draw.rect(surface, color, (bar_x, bar_y, fill_w, bar_h), border_radius=6)

    xp_surf = font_xp.render(
        f"{xp_data.xp_in_level} / {xp_data.xp_to_next_level} XP",
        True, (180, 180, 180)
    )
    surface.blit(xp_surf, (95, 58))

def _draw_btn(surface, label, cx, cy, color, font):
    w, h = font.size(label)
    rect = pygame.Rect(cx - w // 2 - 10, cy - h // 2 - 6, w + 20, h + 12)
    pygame.draw.rect(surface, (20, 20, 20), rect, border_radius=8)
    pygame.draw.rect(surface, color, rect, width=2, border_radius=8)
    text_surf = font.render(label, True, color)
    surface.blit(text_surf, (cx - w // 2, cy - h // 2))

def _start_phase(user, phase, difficulty, mod, tipo, tipo_2players, storyManager):
    from Game.GameManager.GameManager import ManageGame
    song = phase.song
    if mod == "2 Players" and tipo_2players == "Contra":
        gameManager = ManageGame(user, song.file_path, mod, 1, song.file_path, tipo_2players)
    else:
        gameManager = ManageGame(user, song.file_path, mod, 1,phase_number=phase.number)
    gameManager.load_to_run(tipo)
    storyManager.complete_phase(user.id, difficulty.id, song.id, phase.number, tipo)