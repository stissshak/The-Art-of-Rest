# game/engine/input_handler.py

import pygame

class InputHandler:
    def __init__(self):
        # pygame.key.get_pressed() returns a ScancodeWrapper indexed by keycode.
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pos = (0, 0)
        self.mouse_buttons = (False, False, False)

    def update(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_buttons = pygame.mouse.get_pressed()

    def is_key_down(self, key):
        return bool(self.keys_pressed[key])
    
    def is_key_just_pressed(self, key, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == key:
                return True
        return False