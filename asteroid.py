from circleshape import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width=2) #or (self.position.x, self.position.y) for coordinates

    def update(self, dt):
        self.position += (self.velocity * dt)