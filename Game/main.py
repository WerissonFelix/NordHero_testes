import pygame

from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

mixer.init()


class Key:
    def __init__(self, x, y, color1, color2, key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x,self.y,100,40)
        self.active = True

keys = [
    Key(200,500,(255,0,0), (220,0,0),pygame.K_a),
    Key(300,500,(0,255,0), (0,220,0),pygame.K_s),
    Key(400,500,(0,0,255), (0,0,220),pygame.K_d),
    Key(500,500,(255,255,0), (220,220,0),pygame.K_f),
]

def load(mapp):
    rects = []
    mixer.music.load(mapp + ".mp3")
    mixer.music.play()
    file = open(mapp + ".txt", 'r')
    data = file.readlines()

    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '0':
                rect_x = 200 + (x * 100)  # Alinha com as teclas
                rect_y = y * -100
                rects.append(pygame.Rect(rect_x, rect_y, 50, 25))
    return rects

map_rect = load("abolish the IRS")
score = 0
font = pygame.font.Font("freesansbold.ttf", 20)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


    screen.fill((0,0,0))

    keys_pressed = pygame.key.get_pressed()

    for key in keys:
        # Verifica se a tecla está pressionada
        if key.active:
            if keys_pressed[key.key]:
                pygame.draw.rect(screen, key.color2, key.rect)
                key.handled = True
            else:
                pygame.draw.rect(screen, key.color1, key.rect)
                key.handled = False

    rects_to_remove = []


    for rect in map_rect:
        pygame.draw.rect(screen, (200,0,0),rect)
        rect.y += 5
        for key in keys:
            if key.active and key.rect.colliderect(rect):
                if keys_pressed[key.key]:
                    rects_to_remove.append(rect)
                    key.active = True
                    score += 100
                    break


        if rect.y > 600:
            rects_to_remove.append(rect)

    for rect in rects_to_remove:
        if rect in map_rect:
            map_rect.remove(rect)




    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (10, 10))
    pygame.display.update()
    clock.tick(60)