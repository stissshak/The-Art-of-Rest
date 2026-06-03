# game/physics/physics_engine.py

import math
import pygame
from config import Config


class PhysicsEngine:
    def __init__(self, terrain=None):
        self.gravity = Config.GRAVITY
        self.entities = []
        self.terrain = terrain

    def set_terrain(self, terrain):
        self.terrain = terrain

    def add_entity(self, entity):
        self.entities.append(entity)

    def update(self, dt):
        for entity in self.entities:
            if not hasattr(entity, 'velocity'):
                continue

            entity.velocity.y += self.gravity * dt
            if entity.velocity.y > Config.MAX_FALL_SPEED:
                entity.velocity.y = Config.MAX_FALL_SPEED

            if self.terrain is None:
                entity.position += entity.velocity * dt
                continue

            self._move_x(entity, dt)
            self._move_y(entity, dt)

            if hasattr(entity, 'on_ground'):
                probe = entity.get_rect()
                probe.y += 1
                entity.on_ground = self.terrain.rect_collides(probe)

    def _move_x(self, entity, dt):
        delta = entity.velocity.x * dt
        if delta == 0:
            return
        start_x = entity.position.x
        start_y = entity.position.y
        entity.position.x += delta

        if not self.terrain.rect_collides(entity.get_rect()):
            return

        # Blocked: try to climb the slope/step (up to MAX_STEP px).
        climbed = 0
        for s in range(1, Config.MAX_STEP + 1):
            entity.position.y -= 1
            if not self.terrain.rect_collides(entity.get_rect()):
                climbed = s
                break
        else:
            # Genuine wall: drop back down, back out along x and stop.
            entity.position.y = start_y
            step = 1 if delta < 0 else -1
            for _ in range(int(abs(delta)) + 2):
                if not self.terrain.rect_collides(entity.get_rect()):
                    break
                entity.position.x += step
            entity.velocity.x = 0
            return

        # Climbing adds a vertical leg, so the diagonal travel is longer than a
        # flat step. Scale the move down so along-slope distance == walk distance.
        scale = abs(delta) / math.hypot(delta, climbed)
        entity.position.x = start_x + delta * scale
        entity.position.y = start_y - climbed * scale

        # Sit flush on the slope we just climbed: lift out if embedded, else
        # settle down onto it (capped, so this never follows downhill drops).
        if self.terrain.rect_collides(entity.get_rect()):
            for _ in range(Config.MAX_STEP + 1):
                entity.position.y -= 1
                if not self.terrain.rect_collides(entity.get_rect()):
                    break
        else:
            for _ in range(climbed + 2):
                entity.position.y += 1
                if self.terrain.rect_collides(entity.get_rect()):
                    entity.position.y -= 1
                    break

    def _move_y(self, entity, dt):
        delta = entity.velocity.y * dt
        if delta == 0:
            return
        entity.position.y += delta

        if not self.terrain.rect_collides(entity.get_rect()):
            return

        step = 1 if delta < 0 else -1
        for _ in range(int(abs(delta)) + 2):
            if not self.terrain.rect_collides(entity.get_rect()):
                break
            entity.position.y += step
        entity.velocity.y = 0
