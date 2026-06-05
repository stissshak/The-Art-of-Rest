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

        self.width = 20
        self.height = 30
        self.on_ground = False
        self.facing_right = True

        self.move_dir = 0          # -1 left, 0 idle, 1 right
        self.move_speed = Config.PLAYER_SPEED
        self.ground_accel = Config.GROUND_ACCEL
        self.air_accel = Config.AIR_ACCEL
        self.ground_time = 0.0     # seconds continuously grounded (gates jumps)

        # Ninja rope: when roped the worm hangs from rope_anchor on a rope_length
        # tether; the physics engine enforces the distance constraint.
        self.roped = False
        self.rope_anchor = None
        self.rope_length = 0.0

        self.color = self._get_team_color()
        self.name = f"Worm {team}"

    def _get_team_color(self):
        colors = [
            (255, 100, 100),  # Red team
            (100, 100, 255),  # Blue team
            (100, 255, 100),  # Green team
            (255, 255, 100),  # Yellow team
        ]
        return colors[self.team % len(colors)]

    def handle_input(self, input_handler, events):
        self.move_dir = 0
        if input_handler.is_key_down(pygame.K_a) or input_handler.is_key_down(pygame.K_LEFT):
            self.move_dir = -1
            self.facing_right = False
        elif input_handler.is_key_down(pygame.K_d) or input_handler.is_key_down(pygame.K_RIGHT):
            self.move_dir = 1
            self.facing_right = True

        if self.on_ground and self.ground_time >= Config.JUMP_COOLDOWN:
            facing = 1 if self.facing_right else -1
            if input_handler.is_key_just_pressed(pygame.K_SPACE, events):
                self.velocity.x = facing * Config.JUMP_FWD_VX
                self.velocity.y = Config.JUMP_FWD_VY
                self.on_ground = False
            elif input_handler.is_key_just_pressed(pygame.K_LSHIFT, events):
                self.velocity.x = -facing * Config.BACKFLIP_VX
                self.velocity.y = Config.BACKFLIP_VY
                self.on_ground = False

    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.position.x + self.width / 2,
                              self.position.y + self.height / 2)

    def attach_rope(self, anchor: pygame.Vector2, length: float):
        self.roped = True
        self.rope_anchor = pygame.Vector2(anchor)
        self.rope_length = length
        self.on_ground = False

    def detach_rope(self):
        self.roped = False
        self.rope_anchor = None

    def update(self, dt: float):
        # Grounded time gates the jump cooldown; resets the moment we're airborne.
        self.ground_time = self.ground_time + dt if self.on_ground else 0.0

        # Roped: A/D add a tangential push so the worm pumps the swing. The
        # rope-length constraint itself lives in the physics engine.
        if self.roped and self.rope_anchor is not None:
            offset = self.center() - self.rope_anchor
            if offset.length_squared() > 0 and self.move_dir != 0:
                tangent = pygame.Vector2(offset.y, -offset.x).normalize()
                self.velocity += tangent * self.move_dir * Config.ROPE_SWING_ACCEL * dt
            return

        # Ease toward the input target on the ground; in the air keep jump
        # momentum unless actively steering.
        if self.on_ground:
            target = self.move_dir * self.move_speed
            self.velocity.x = _approach(self.velocity.x, target, self.ground_accel * dt)
        elif self.move_dir != 0:
            target = self.move_dir * self.move_speed
            self.velocity.x = _approach(self.velocity.x, target, self.air_accel * dt)

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


def _approach(value, target, max_delta):
    if value < target:
        return min(value + max_delta, target)
    return max(value - max_delta, target)
