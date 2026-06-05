# main.py

import math
import pygame
from config import Config
from game.engine.input_handler import InputHandler
from game.engine.turn_manager import TurnManager
from game.physics.physics_engine import PhysicsEngine
from game.entities.entities_manager import EntityManager
from game.entities.player import Player
from game.entities.projectile import Projectile
from game.world.terrain import Terrain

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("The-Art-Of-Rest")
        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 96)

        self.input_handler = InputHandler()
        self.entity_manager = EntityManager()
        self.terrain = Terrain()
        self.physics_engine = PhysicsEngine(self.terrain)

        self._create_players()
        self.entity_manager.flush()
        self.turn_manager = TurnManager(self.entity_manager, Config.TURN_TIME)

        # Weapon state (reset each turn)
        self._weapon_turn = -1
        self.charging = False
        self.power = 0.0
        self.has_fired = False
        self.retreat_timer = None
        self.explosions = []          # [x, y, age] short-lived blast flashes
        self.aim_angle = 45.0         # elevation in degrees for keyboard aiming
    
    def _create_players(self):
        # Team 1 (Red)
        team1_positions = [
            pygame.Vector2(300, 400),
            pygame.Vector2(400, 400),
        ]
        
        # Team 2 (Blue)
        team2_positions = [
            pygame.Vector2(1520, 400),
            pygame.Vector2(1620, 400),
        ]
        
        for pos in team1_positions:
            player = Player(pos, team=0)
            self.entity_manager.add(player)
            self.physics_engine.add_entity(player)
        
        for pos in team2_positions:
            player = Player(pos, team=1)
            self.entity_manager.add(player)
            self.physics_engine.add_entity(player)
    
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.turn_manager.end_turn()

        self.input_handler.update()

        # Only the active worm takes input; everyone else holds still.
        for player in self.entity_manager.get_entities_of_type(Player):
            player.move_dir = 0
        active = self.turn_manager.active_player
        if active and not self.turn_manager.game_over:
            active.handle_input(self.input_handler, events)

    def update(self, dt: float):
        self.entity_manager.update(dt)
        self.physics_engine.update(dt)
        self.turn_manager.update(dt)

        if self.turn_manager.turn_number != self._weapon_turn:
            self._reset_weapon()
        self._update_weapon(dt)
        self._update_retreat(dt)
        for blast in self.explosions:
            blast[2] += dt
        self.explosions = [b for b in self.explosions if b[2] < 0.25]

    def _reset_weapon(self):
        self._weapon_turn = self.turn_manager.turn_number
        self.charging = False
        self.power = 0.0
        self.has_fired = False
        self.retreat_timer = None
        self.aim_angle = 45.0

    def _update_weapon(self, dt: float):
        tm = self.turn_manager
        player = tm.active_player
        if tm.game_over or player is None or self.has_fired:
            self.charging = False
            return

        ih = self.input_handler

        if not self.charging:
            up = ih.is_key_down(pygame.K_UP) or ih.is_key_down(pygame.K_w)
            down = ih.is_key_down(pygame.K_DOWN) or ih.is_key_down(pygame.K_s)
            if up or down:
                self.aim_mode = 'keyboard'
                self.aim_angle += (up - down) * Config.AIM_SPEED * dt
                self.aim_angle = max(-85.0, min(85.0, self.aim_angle))

        # Charge while LMB or F is held, fire on release.
        firing_held =  ih.is_key_down(pygame.K_f)
        if firing_held:
            if not self.charging:
                self.charging = True
                self.power = Config.PROJECTILE_MIN_POWER
            else:
                self.power = min(self.power + Config.CHARGE_RATE * dt, Config.PROJECTILE_MAX_POWER)
        elif self.charging:
            self._fire(player)
            self.charging = False
            self.has_fired = True

    def _aim_dir(self, player, origin):
        ang = math.radians(self.aim_angle)
        face = 1 if player.facing_right else -1
        return pygame.Vector2(math.cos(ang) * face, -math.sin(ang))

    def _fire(self, player):
        origin = pygame.Vector2(player.position.x + player.width / 2,
                                player.position.y + player.height / 2)
        aim = self._aim_dir(player, origin)
        spawn = origin + aim * 24
        shell = Projectile(spawn, aim * self.power, self.terrain,
                           self.entity_manager, self._explode, shooter=player)
        self.entity_manager.add(shell)

    def _explode(self, x, y):
        self.terrain.destroy_circle(x, y, Config.EXPLOSION_RADIUS)
        blast = pygame.Vector2(x, y)
        radius = Config.EXPLOSION_RADIUS
        for player in self.entity_manager.get_entities_of_type(Player):
            center = pygame.Vector2(player.position.x + player.width / 2,
                                    player.position.y + player.height / 2)
            dist = (center - blast).length()
            if dist <= radius:
                frac = 1 - dist / radius
                damage = Config.EXPLOSION_EDGE_DAMAGE + \
                    (Config.EXPLOSION_DAMAGE - Config.EXPLOSION_EDGE_DAMAGE) * frac
                player.take_damage(int(damage))
                kick = (center - blast).normalize() if dist > 0 else pygame.Vector2(0, -1)
                player.velocity += kick * Config.KNOCKBACK * frac
                player.on_ground = False
        self.explosions.append([x, y, 0.0])
        self.retreat_timer = Config.RETREAT_TIME

    def _update_retreat(self, dt: float):
        if self.retreat_timer is None:
            return
        self.retreat_timer -= dt
        if self.retreat_timer <= 0:
            self.retreat_timer = None
            self.turn_manager.end_turn()
    
    def render(self):
        self.screen.fill((135, 206, 235))

        self.terrain.draw(self.screen)

        self.entity_manager.draw(self.screen)
        self._draw_explosions()
        self._draw_active_marker()
        self._draw_aim()

        self._draw_ui()

        pygame.display.flip()

    def _draw_explosions(self):
        for x, y, age in self.explosions:
            t = age / 0.25
            outer = int(Config.EXPLOSION_RADIUS * (0.4 + 0.6 * t))
            pygame.draw.circle(self.screen, (255, 160, 40), (int(x), int(y)), outer)
            pygame.draw.circle(self.screen, (255, 230, 120), (int(x), int(y)), max(1, outer - 10))

    def _draw_aim(self):
        tm = self.turn_manager
        player = tm.active_player
        if tm.game_over or player is None or self.has_fired:
            return

        origin = pygame.Vector2(player.position.x + player.width / 2,
                                player.position.y + player.height / 2)
        aim = self._aim_dir(player, origin)
        for i in range(1, 8):
            pt = origin + aim * (20 * i)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(pt.x), int(pt.y)), 2)

        if self.charging:
            span = Config.PROJECTILE_MAX_POWER - Config.PROJECTILE_MIN_POWER
            frac = (self.power - Config.PROJECTILE_MIN_POWER) / span
            bx, by = player.position.x - 5, player.position.y - 28
            pygame.draw.rect(self.screen, (0, 0, 0), (bx, by, 40, 6), 1)
            pygame.draw.rect(self.screen, (255, 80, 80), (bx + 1, by + 1, int(38 * frac), 4))

    def _draw_active_marker(self):
        player = self.turn_manager.active_player
        if not player:
            return
        bob = math.sin(pygame.time.get_ticks() * 0.006) * 4
        cx = player.position.x + player.width / 2
        top = player.position.y - 18 + bob
        points = [(cx - 8, top), (cx + 8, top), (cx, top + 11)]
        pygame.draw.polygon(self.screen, (255, 255, 0), points)

    def _draw_ui(self):
        tm = self.turn_manager

        if tm.game_over:
            msg = "Draw!" if tm.winner is None else f"Team {tm.winner + 1} wins!"
            text = self.big_font.render(msg, True, (255, 255, 255))
            rect = text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
            self.screen.blit(text, rect)
            return

        player = tm.active_player
        if player:
            info = self.font.render(f"Team {player.team + 1} — {player.name}", True, player.color)
            self.screen.blit(info, (20, 20))

        timer = self.font.render(f"{tm.time_left:0.0f}s", True, (0, 0, 0))
        self.screen.blit(timer, (Config.SCREEN_WIDTH // 2 - 20, 20))
    
    def run(self):
        while self.running:
            dt = self.clock.tick(Config.FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
