# game/physics/physics_engine.py

import pygame
from config import Config

class PhysicsEngine:
    def __init__(self):
        self.gravity = Config.GRAVITY
        self.entities = []
    
    def add_entity(self, entity):
        self.entities.append(entity)
    
    def update(self, dt):
        for entity in self.entities:
            if hasattr(entity, 'velocity'):
                entity.velocity.y += self.gravity * dt
                
                if entity.velocity.y > Config.MAX_FALL_SPEED:
                    entity.velocity.y = Config.MAX_FALL_SPEED
                
                entity.position += entity.velocity * dt