import pygame
import random
from constants import *

class PowerUp(pygame.sprite.Sprite):
    containers = None  # This ensures the sprite is added to the correct groups.

    def __init__(self):
        super().__init__(self.containers)  # Automatically adds the sprite to the groups.
        self.position = pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * 50
        self.image = pygame.Surface((POWER_UP_SIZE, POWER_UP_SIZE))
        self.image.fill("white")  # Default color; subclasses can override.
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt):
        # Move the power-up.
        self.position += self.velocity * dt
        self.rect.center = self.position

        # Check if the power-up is out of bounds and wrap it around the screen.
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def draw(self, screen):
        """Draws the power-up on the screen."""
        screen.blit(self.image, self.rect)


class ShieldPowerUp(PowerUp):
    def __init__(self):
        super().__init__()
        self.image.fill(SHIELD_COLOR)  # Set the color for Shield power-ups.

class SpeedPowerUp(PowerUp):
    def __init__(self):
        super().__init__()
        self.image.fill(SPEED_COLOR)  # Set the color for Speed power-ups.

class BombPowerUp(PowerUp):
    def __init__(self):
        super().__init__()
        self.image.fill(BOMB_COLOR)  # Set the color for Bomb power-ups.
