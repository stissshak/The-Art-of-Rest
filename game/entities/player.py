# game/entities/player.py

import pygame
from .entity import Entity
from config import Config

class Player(Entity):
    def __init__(self, position: pygame.Vector2, team: int = 0):
        super().__init__(position)

        self.hp = 100
        self.max_hp = 100
        self.team = team
        self.feet_y = self.position.y + self.height / 2
        self.head_y = self.position.y + self.height / 2
        

        self.width = 20
        self.height = 30
        self.on_ground = False
        self.facing_right = True

        self.move_speed = Config.PLAYER_SPEED
        self.jump_force = Config.JUMP_FORCE

        self.color = self._get_team_color()
        self.name = f"Worm {team}"

    def _get_team_color(self):
        colors = [
            (255, 100, 100),  # Read team
            (100, 100, 255),  # Blue team
            (100, 255, 100),  # Green team
            (255, 255, 100),  # Yellow team
        ]
        return colors[self.team % len(colors)]
    
    def handle_input(self, input_handler, events):
        if input_handler.is_key_down(pygame.K_a):
            self.velocity.x = -self.move_speed
            self.facing_right = False
        elif input_handler.is_key_down(pygame.K_d):
            self.velocity.x = self.move_speed
            self.facing_right = True
        else:
            self.velocity.x = 0
        
        if input_handler.is_key_just_pressed(pygame.K_SPACE, events) and self.on_ground:
            self.velocity.y = self.jump_force
            self.on_ground = False

    def update(self, dt: float):
        # In PhysicsEngine
        pass

    def on_collision(self, terrain):
        rect = self.get_rect()
        
        if self.velocity.y > 0:
            self.on_ground = True
            self.velocity.y = 0

    def take_damage(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.destroy()
    
    def heal(self, amount: int):
        self.hp = min(self.hp + amount, self.max_hp)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, (self.position.x, self.position.y, self.width, self.height), width=1)
        self._draw_hp_bar(screen)
    
    def _draw_hp_bar(self, screen: pygame.Surface):
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.hp), True, self.color)
        screen.blit(text, (self.position + (0, -self.height / 2)))