# game/entities/entities_manager.py

from typing import List, Type
from .entity import Entity

class EntityManager:
    """ Manager for all game's objects """"
    
    def __init__(self):
        self.entities: List[Entity] = []
        self._to_add: List[Entity] = []
        self._to_remove: List[Entity] = []
    
    def add(self, entity: Entity):
        if not isinstance(entity, Entity):
            raise TypeError(f"Expected Entity, got {type(entity).__name__}")
        self._to_add.append(entity)
    
    def remove(self, entity: Entity):
        if not isinstance(entity, Entity):
            raise TypeError(f"Expected Entity, got {type(entity).__name__}")
        self._to_remove.append(entity)
    
    def update(self, dt: float):
        if self._to_add:
            self.entities.extend(self._to_add)
            self._to_add.clear()
        
        for entity in self.entities:
            if entity.active:
                entity.update(dt)
        
        self.entities = [e for e in self.entities 
                        if e.active and e not in self._to_remove]
        self._to_remove.clear()

    def draw(self, screen):
        for entity in self.entities:
            if entity.active:
                entity.draw(screen)
    
    def get_entities_of_type(self, entity_type: Type[Entity]) -> List[Entity]:
        return [e for e in self.entities if isinstance(e, entity_type)]
    
    def clear(self):
        self.entities.clear()
        self._to_add.clear()
        self._to_remove.clear()