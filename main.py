import pygame
from constants import *
from player import *


def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    while True:
        #limit game FPS to 60
        dt = clock.tick(60) / 1000

        #Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # Update game objects
        player.update(dt)

        # Draw everything
        screen.fill("black")
        player.draw(screen)
        # Draw other game objects...

        pygame.display.flip()


if __name__ == "__main__":
    main()