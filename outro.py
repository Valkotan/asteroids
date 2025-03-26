import pygame
import sys
from main import save_scores
from score import *
from constants import *



def show_outro_screen(screen, font, current_score, top_scores):
    # Update top scores list
    top_scores.append(current_score)
    top_scores = sorted(top_scores, reverse=True)[:3]  # Keep only the top 3 scores

    # Save updated scores to a file
    with open("top_scores.txt", "w") as file:
        for score in top_scores:
            file.write(f"{score}\n")

    screen.fill("black")

    title_text = font.render("Game Over!", True, "white")
    screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 100))

    score_text = font.render(f"Your Score: {current_score:04}", True, "white")
    screen.blit(score_text, (SCREEN_WIDTH / 2 - score_text.get_width() / 2, 200))

    top_scores_title = font.render("Top Scores:", True, "white")
    screen.blit(top_scores_title, (SCREEN_WIDTH / 2 - top_scores_title.get_width() / 2, 300))

    y_offset = 350
    for i, score in enumerate(top_scores):
        score_entry = font.render(f"{i + 1}. {score:04}", True, "white")
        screen.blit(score_entry, (SCREEN_WIDTH / 2 - score_entry.get_width() / 2, y_offset))
        y_offset += 50

    restart_text = font.render("Press SPACEBAR to restart or ESC to exit", True, "white")
    screen.blit(restart_text, (SCREEN_WIDTH / 2 - restart_text.get_width() / 2, y_offset + 50))

    pygame.display.flip()

    # Wait for the player to press SPACEBAR to restart or ESC to quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Restart the game
                    return True  # Signal to restart the game
                elif event.key == pygame.K_ESCAPE:  # Exit the game
                    pygame.quit()
                    sys.exit()

