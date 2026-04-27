# game/engine/game_state.py

from enum import Enum

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PLAYER_TURN = 3
    WEAPON_SELECT = 4
    PAUSED = 5

class StateManager:
    def __init__(self):
        self.current_state = GameState.MENU
        self.states = {}
    
    def change_state(self, new_state):
        if self.current_state in self.states:
            self.states[self.current_state].exit()
        self.current_state = new_state
        if new_state in self.states:
            self.states[new_state].enter()