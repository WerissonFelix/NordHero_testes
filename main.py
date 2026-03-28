import pygame


from Screens.Inital import initial_screen
from Screens.Logon import login_screen
from Screens.Creat_Account import create_account_menu
pygame.init()
surface = pygame.display.set_mode((600, 400))
initial_screen(login_screen,create_account_menu)