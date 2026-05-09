import pygame
import pygame_menu
from Game.Config.Game_Config import GameConfig
from Screens.Pause import pause_menu

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def change_controls_menu(config):

    initial_menu = pygame_menu.Menu(
        '',
        800,
        600,
        theme=pygame_menu.themes.THEME_BLUE)

    modo_captura = False

    key_changed = "key1"

    running = True
    
    keys = {
        "key1": config.key1,
        "key2": config.key2,
        "key3": config.key3,
        "key4": config.key4
    }
    
    def uptade_key(Key):
        nonlocal modo_captura, key_changed
        modo_captura = True    
        key_changed = Key

    def change_key(new_key):
        nonlocal modo_captura, key_changed, keys
        modo_captura = False
        print(new_key)
        keys[key_changed] = new_key
        af = pygame.key.name(new_key)
        initial_menu.add.label(f"new key: {af}")

    def chance_config_key():
        nonlocal keys, initial_menu,running 
        config.key1 = keys["key1"]
        config.key2 = keys["key2"]
        config.key3 = keys["key3"]
        config.key4 = keys["key4"]
             
        running = False
        
        print(config.key1,config.key2, config.key3, config.key4)
        
        initial_menu.disable()     
        
        #pause_menu(user, music_path, total_notes, notes_hit, initial_menu)
        
    for k, v in keys.items():
        initial_menu.add.label(f"key {k}: {pygame.key.name(v)}")
        initial_menu.add.button('Alterar', uptade_key, k)  
        
    initial_menu.add.button('Confirmar', chance_config_key) 
    initial_menu.add.button('BACK', initial_menu.disable) 

    initial_menu.enable()
    
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if modo_captura:            
                if event.type == pygame.KEYDOWN:   
                    change_key(event.key)

        if initial_menu.is_enabled():     
            initial_menu.draw(screen)       
            initial_menu.update(events)     
        else:
            running = False
             
        pygame.display.flip()
        clock.tick(60)  