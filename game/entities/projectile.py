# game/entities/projectile.py

import pygame
from .entity import Entity
from .player import Player
from config import Config


class Projectile(Entity):
    def __init__(self, position, velocity, terrain, entity_manager, on_detonate, shooter=None):
        super().__init__(pygame.Vector2(position))
        self.velocity = pygame.Vector2(velocity)
        self.terrain = terrain
        self.entity_manager = entity_manager
        self.on_detonate = on_detonate
        self.shooter = shooter

        self.width = 6
        self.height = 6
        self._done = False

    def update(self, dt: float):
        self.velocity.y += Config.GRAVITY * dt
        self.position += self.velocity * dt
        x, y = int(self.position.x), int(self.position.y)

        if y >= Config.SCREEN_HEIGHT or x < 0 or x >= Config.SCREEN_WIDTH:
            self._detonate()
            return
        if self.terrain.is_solid(x, y):
            self._detonate()
            return
        for p in self.entity_manager.get_entities_of_type(Player):
            if p is not self.shooter and p.get_rect().collidepoint(self.position):
                self._detonate()
                return

    def _detonate(self):
        if self._done:
            return
        self._done = True
        self.on_detonate(self.position.x, self.position.y)
        self.destroy()

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, (35, 35, 35), (int(self.position.x), int(self.position.y)), 4)
