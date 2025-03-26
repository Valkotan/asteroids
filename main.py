import sys
import pygame
import random
from constants import *
from player import Player
from asteroid import *
from asteroidfield import *
from score import ScoreManager
from shot import * 
from powerups import ShieldPowerUp, SpeedPowerUp, BombPowerUp
from intro import show_intro_screen
from outro import *

# Functions for persistence
def save_scores(top_scores):
    """Save top scores to a file."""
    with open("top_scores.txt", "w") as file:
        for score in top_scores:
            file.write(f"{score}\n")

def load_scores():
    """Load top scores from a file."""
    try:
        with open("top_scores.txt", "r") as file:
            return [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return []

def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)

    # Load top scores from a persistent file
    top_scores = load_scores()

    while True:  # Outer loop for restarting the game
        # Show the intro screen
        show_intro_screen(screen, font)

        # Reinitialize game state
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        power_ups = pygame.sprite.Group()

        # Set containers for game objects
        Shot.containers = (shots, updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable,)
        asteroid_field = AsteroidField()

        Player.containers = (updatable, drawable)
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        score_manager = ScoreManager()

        ShieldPowerUp.containers = (power_ups, updatable, drawable)
        SpeedPowerUp.containers = (power_ups, updatable, drawable)
        BombPowerUp.containers = (power_ups, updatable, drawable)

        power_up_active = False  # Tracks whether a power-up is currently active

        game_active = True  # Flag to control the inner game loop

        while game_active:
            # Limit game FPS to 60
            dt = clock.tick(60) / 1000

            # Spawn a power-up if none is active
            if not power_up_active and not power_ups and random.random() < POWER_UP_SPAWN_RATE:
                power_up_type = random.choice([ShieldPowerUp, SpeedPowerUp, BombPowerUp])
                power_up_type()
                power_up_active = True  # Mark that a power-up has spawned

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update game objects
            updatable.update(dt)

            # Check for collisions between asteroids and the player
            for asteroid in asteroids:
                if asteroid.collision(player):
                    if player.shield_active > 0:  # If the shield is active
                        score_manager.increment_score(extra_points=20)
                        asteroid.kill()  # Destroy the asteroid
                    else:
                        # Game over
                        current_score = score_manager.get_score()
                        restart = show_outro_screen(screen, font, current_score, top_scores)
                        if restart:
                            game_active = False  # Exit inner loop to restart
                        else:
                            pygame.quit()
                            sys.exit()

            # Check for collisions between shots and asteroids
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collision(asteroid):
                        shot.kill()
                        if shot.is_bomb:  # Check if the shot is a bomb
                            score_manager.increment_score(extra_points=30)  # Award bonus points
                            asteroid.kill()  # Instantly destroy the asteroid
                        else:
                            score_manager.increment_score()
                            asteroid.split()

            # Check for power-up collisions with the player
            for power_up in power_ups:
                player_collision = player.position.distance_to(power_up.position) < (POWER_UP_SIZE + PLAYER_RADIUS)
                if player_collision:
                    player.apply_power_up(power_up)
                    power_up.kill()
                    power_up_active = True  # Power-up is active

            # Check if the active power-up has expired
            if player.shield_active <= 0 and player.speed_boosted <= 0 and player.bomb_equipped <= 0:
                power_up_active = False  # Reset power-up state

            # Draw everything
            screen.fill("black")
            for sprite in drawable:
                sprite.draw(screen)

            # Display the current score
            score_text = font.render(f"Score: {score_manager.get_score():04}", True, "white")
            screen.blit(score_text, (10, 10))

            pygame.display.flip()

if __name__ == "__main__":
    main()
