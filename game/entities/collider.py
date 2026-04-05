import math

class Collider:
    def __init__(self, height, width, x = 0, y = 0):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
    
    def if_collide(self, other):
        if (math.abs(self.x - other.x) <= (self.width + other.width) / 2 or math.abs(self.y - other.y) <= (self.height + other.height) / 2):
            return True
        else:
            return False
        
    def on_ground(self):
        # TODO
        pass    

    