import sys
import pygame
from constants import *


def show_intro_screen(screen, font):
        screen.fill("black")

        title_text = font.render("Welcome to the Asteroid Game!", True, "white")
        screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 100))

        instructions = [
            ("Power-Up Guide", "white"),
            ("Shield Power-Up: Protects you from asteroids (Color: Blue)", SHIELD_COLOR),
            ("Speed Power-Up: Boosts your speed (Color: Green)", SPEED_COLOR),
            ("Bomb Power-Up: Destroys asteroids instantly (Color: Red)", BOMB_COLOR),
            ("Press SPACEBAR to start the game", "white"),
        ]

        y_offset = 200
        for text, color in instructions:
            rendered_text = font.render(text, True, color)
            screen.blit(rendered_text, (SCREEN_WIDTH / 2 - rendered_text.get_width() / 2, y_offset))
            y_offset += 50

        pygame.display.flip()

        # Wait for the player to press SPACEBAR
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False