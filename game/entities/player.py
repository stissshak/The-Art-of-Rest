import Object from object

class Player(Object):
    def __init__(self, vector, collider, sprite):
        self.pos = vector
        self.collider = collider
        self.sprite = sprite

    def set_hp(self, hp):
        if (hp < 0):
            raise ValueError("HP cannot be negative")
        self.hp = hp
