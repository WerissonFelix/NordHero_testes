import pygame

from Screens.Inital import initial_screen
from Screens.Logon import login_screen
from Screens.Creat_Account import create_account_menu
from Features.audio.music_loader import load_and_register_music
from DataBase.tables import create_all


create_all()
load_and_register_music()
pygame.init()
surface = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("NORD HERO")
initial_screen(login_screen, create_account_menu)