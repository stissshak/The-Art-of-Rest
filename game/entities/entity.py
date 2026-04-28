# game/enities/entity.py

import pygame
from typing import Optional

class Entity:
    def __init__(self, position: pygame.Vector2):
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

        self.width = 32
        self.height = 32
        self.active = True

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.position.x - self.width // 2,
            self.position.y - self.height // 2,
            self.width,
            self.height
        )
    
    def update(self, dt: float):
        # Will be overrided
        pass
    
    def draw(self, screen: pygame.Surface):
        # Will be overrided
        pass
    
    def destroy(self):
        self.active = False

