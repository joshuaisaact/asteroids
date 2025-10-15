import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def start_screen(screen, font, title_font, top_score):
    while True:
        screen.fill("black")

        # Draw title
        title_text = title_font.render("Pysteroids", True, "white")
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        screen.blit(title_text, title_rect)

        # Draw menu options
        new_game_text = font.render("New Game", True, "white")
        new_game_rect = new_game_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(new_game_text, new_game_rect)

        exit_text = font.render("Exit", True, "white")
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))
        screen.blit(exit_text, exit_rect)

        # Draw top score
        top_score_text = font.render(f"Top Score: {top_score}", True, "white")
        top_score_rect = top_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 300))
        screen.blit(top_score_text, top_score_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if new_game_rect.collidepoint(mouse_pos):
                    return "new_game"
                if exit_rect.collidepoint(mouse_pos):
                    return "exit"

def game_loop(screen, clock, font, top_score):
    score = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, top_score

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print(f"Game over! Final score: {score}")
                if score > top_score:
                    top_score = score
                return True, top_score

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    score += 1
                    asteroid.kill()
                    shot.kill()
                    asteroid.split()
                    break

        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)

        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    top_score = 0

    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 74)

    while True:
        # Show start screen
        choice = start_screen(screen, font, title_font, top_score)
        if choice == "exit":
            break

        # Run game
        continue_playing, top_score = game_loop(screen, clock, font, top_score)
        if not continue_playing:
            break

    pygame.quit()


if __name__ == "__main__":
    main()

