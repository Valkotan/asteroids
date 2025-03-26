import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot  # Ensure you import the Shot class
from powerups import ShieldPowerUp, SpeedPowerUp, BombPowerUp

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.shield_active = 0  # Timer for shield power-up duration
        self.speed_boosted = 0  # Timer for speed power-up duration
        self.bomb_equipped = 0  # Timer for bomb power-up duration
        self.color = "white"  # Default player color

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.triangle(), width=2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        # Keep rotation within [0, 360) degrees
        self.rotation %= 360

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if self.timer > 0:
            self.timer -= dt

        # Process movement and rotation based on key input
        speed_multiplier = PLAYER_SPEED * (2 if self.speed_boosted > 0 else 1)
        if keys[pygame.K_w]:
            self.move(dt * speed_multiplier)
        if keys[pygame.K_s]:
            self.move(-dt * speed_multiplier)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Update power-up effects
        if self.shield_active > 0:
            self.shield_active -= dt
        if self.speed_boosted > 0:
            self.speed_boosted -= dt
        if self.bomb_equipped > 0:
            self.bomb_equipped -= dt

        # Revert player color if no power-up is active
        if self.shield_active <= 0 and self.speed_boosted <= 0 and self.bomb_equipped <= 0:
            self.color = "white"

        # Bound the player's position so that they remain inside the window
        self.bound_to_screen()

    def apply_power_up(self, power_up):
        if isinstance(power_up, ShieldPowerUp):
            self.shield_active = 7  # Shield lasts for 7 seconds
            self.color = SHIELD_COLOR
        elif isinstance(power_up, SpeedPowerUp):
            self.speed_boosted = 7  # Speed boost lasts for 7 seconds
            self.color = SPEED_COLOR
        elif isinstance(power_up, BombPowerUp):
            self.bomb_equipped = 7  # Bomb lasts for 7 seconds
            self.color = BOMB_COLOR

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * dt

    def bound_to_screen(self):
        """Constrains the player's position so that they remain fully visible within the game window."""
        # Horizontal boundaries
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
        elif self.position.x + self.radius > SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH - self.radius
        
        # Vertical boundaries
        if self.position.y - self.radius < 0:
            self.position.y = self.radius
        elif self.position.y + self.radius > SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT - self.radius

    def shoot(self):
        # Enforce shooting cooldown
        if self.timer > 0:
            return 
        
        # Reduce cooldown duriing speed boost
        base_cooldown = PLAYER_SHOOT_COOLDOWN
        cooldown = base_cooldown * (0.5 if self.speed_boosted > 0 else 1) # Halve the cooldown

        self.timer = cooldown
        
        # Create a shot at the current player position
        shot = Shot(self.position.x, self.position.y)

        # Calculate the shot's velocity based on the current player's rotation
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

        # Bomb behavior: instantly destroys asteroids and awards extra points
        if self.bomb_equipped > 0:
            shot.is_bomb = True
        return shot
