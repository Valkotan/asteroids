import pygame
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, is_bomb=False):
        super().__init__(x, y, SHOT_RADIUS)
        self.rotation = 0
        self.is_bomb = is_bomb  # Add the is_bomb attribute with a default value of False

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # Change color based on whether it's a bomb shot
        color = "red" if self.is_bomb else "white"
        pygame.draw.polygon(screen, color, self.triangle(), width=2)

    def update(self, dt):
        self.position += (self.velocity * dt)