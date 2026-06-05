# game/engine/input_handler.py

import pygame

class InputHandler:
    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()

    def update(self):
        self.keys_pressed = pygame.key.get_pressed()

    def is_key_down(self, key):
        return bool(self.keys_pressed[key])
    
    def is_key_just_pressed(self, key, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == key:
                return True
        return False
