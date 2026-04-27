# main.py

import pygame
from config import Config
from game.engine.input_handler import InputHandler
from game.physics.physics_engine import PhysicsEngine
from game.entities.entity_manager import EntityManager
from game.entities.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("The-Art-Of-Rest")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.input_handler = InputHandler()
        self.entity_manager = EntityManager()
        self.physics_engine = PhysicsEngine()
        
        self._create_players()
        self.current_player_index = 0
    
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
    
    def get_current_player(self) -> Player:
        players = self.entity_manager.get_entities_of_type(Player)
        if players:
            return players[self.current_player_index % len(players)]
        return None
    
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    # Debug feature
                    players = self.entity_manager.get_entities_of_type(Player)
                    self.current_player_index = (self.current_player_index + 1) % len(players)
        
        self.input_handler.update()
        
        current_player = self.get_current_player()
        if current_player:
            current_player.handle_input(self.input_handler, events)
    
    def update(self, dt: float):
        self.physics_engine.update(dt)
        self.entity_manager.update(dt)
    
    def render(self):
        self.screen.fill((135, 206, 235))  # Sky (TODO Arhtur)
        
        # Ground (TODO Arthur)
        pygame.draw.rect(self.screen, (100, 200, 100), 
                        (0, 600, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT - 600))
        
        self.entity_manager.draw(self.screen)
        
        # UI
        self._draw_ui()
        
        pygame.display.flip()
    
    def _draw_ui(self):
        # TODO Athrur
        font = pygame.font.Font(None, 36)
        current_player = self.get_current_player()
        if current_player:
            text = font.render(f"Current: {current_player.name}", True, (0, 0, 0))
            self.screen.blit(text, (10, 10))
    
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