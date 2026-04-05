import pygame
from game.entities.objects import ObjectList as OL 
from game.entities.player import Player as Player

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
dt = 0

ol = OL()
p = Player(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), 0, 0)

def handle_input():
    global running, screen, p
    p.move(screen)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

def collisions():
    pass

def render():
    global screen
    pygame.display.flip()


while running:
    handle_input()
    collisions()
    render()

pygame.quit()

