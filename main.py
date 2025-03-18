import sys
import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from score import ScoreManager


def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    score_manager = ScoreManager()
    font = pygame.font.Font(None, 36)

    while True:
        #limit game FPS to 60
        dt = clock.tick(60) / 1000

        #Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # Update game objects
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game over!")
                print(f"Your Score Was: {score_manager.get_score():04}")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if shot.collision(asteroid):
                    shot.kill()
                    score_manager.increment_score()
                    asteroid.split()

        # Draw everything        
        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)
        # Draw other game objects...
        score_text = font.render(f"Score: {score_manager.get_score():04}", True, "white")
        screen.blit(score_text, (10, 10))  # Display the current score


        pygame.display.flip()


if __name__ == "__main__":
    main()