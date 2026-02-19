from objects import Object

class Player(Object):
    def __init__(self, vector, collider, sprite):
        self.pos = vector
        self.collider = collider
        self.sprite = sprite

    def set_hp(self, hp):
        if (hp < 0):
            raise ValueError("HP cannot be negative")
        self.hp = hp

    def move(self, screen):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos.y -= 3
        if keys[pygame.K_s]:
            self.pos.y += 3
        if keys[pygame.K_a]:
            self.pos.x -= 3
        if keys[pygame.K_d]:
            self.pos.x += 3
        pygame.draw.circle(screen, "red", self.pos, 40)
