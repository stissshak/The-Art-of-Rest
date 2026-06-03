# game/engine/turn_manager.py

from game.entities.player import Player


class TurnManager:
    """Rotates control team-by-team; each team cycles through its own worms."""

    def __init__(self, entity_manager, turn_time):
        self.entity_manager = entity_manager
        self.turn_time = turn_time

        self.active_team = -1
        self.active_player = None
        self.time_left = turn_time
        self.turn_number = 0        # bumps each turn; lets others reset per-turn state
        self.game_over = False
        self.winner = None          # team id, or None for a draw
        self._last_worm = {}        # team -> last worm that acted

        self.start_turn()

    def _players(self):
        return [e for e in self.entity_manager.entities if isinstance(e, Player)]

    def _alive_teams(self):
        return sorted({p.team for p in self._players()})

    def _team_worms(self, team):
        return [p for p in self._players() if p.team == team]

    def _next_team(self, current, teams):
        later = [t for t in teams if t > current]
        return later[0] if later else teams[0]

    def _next_worm(self, team):
        worms = self._team_worms(team)
        if not worms:
            return None
        last = self._last_worm.get(team)
        if last in worms:
            nxt = worms[(worms.index(last) + 1) % len(worms)]
        else:
            nxt = worms[0]
        self._last_worm[team] = nxt
        return nxt

    def start_turn(self):
        teams = self._alive_teams()
        if len(teams) <= 1:
            self.game_over = True
            self.winner = teams[0] if teams else None
            self.active_player = None
            return
        self.active_team = self._next_team(self.active_team, teams)
        self.active_player = self._next_worm(self.active_team)
        self.time_left = self.turn_time
        self.turn_number += 1

    def end_turn(self):
        if not self.game_over:
            self.start_turn()

    def is_active(self, player):
        return player is self.active_player

    def update(self, dt):
        if self.game_over:
            return
        teams = self._alive_teams()
        if len(teams) <= 1:                             # a team was wiped out
            self.game_over = True
            self.winner = teams[0] if teams else None
            self.active_player = None
            return
        if self.active_player not in self._players():   # active worm died
            self.end_turn()
            return
        self.time_left -= dt
        if self.time_left <= 0:
            self.end_turn()
