import pygame
import sys
import random

def flappy_bird():
    
    # Game Variables
    gravity = 0.25
    bird_movement = 0
    game_active = True
    score = 0
    high_score = 0

    # Pygame Setup
    pygame.init()
    screen = pygame.display.set_mode((288, 512))
    clock = pygame.time.Clock()

    # Game Assets
    bg_surface = pygame.Surface((288, 512)) 
    bg_surface.fill((135, 206, 235))

    floor_surface = pygame.Surface((288, 32))
    floor_surface.fill((222, 196, 169))
    floor_x_pos = 0
    floor_y_pos = 480  # Position the floor at the bottom of the screen

    bird_surface = pygame.image.load('bird.png').convert_alpha()
    bird_surface = pygame.transform.scale(bird_surface, (34, 34))
    bird_rect = bird_surface.get_rect(center=(50, 256))

    pipe_surface = pygame.Surface((50, 300))
    pipe_surface.fill((0, 255, 0))

    # Pipe class to handle both top and bottom pipes
    class Pipe:
        def __init__(self):
            self.height = random.randint(100, 300)  # Random height for the top pipe
            self.top_rect = pipe_surface.get_rect(midbottom=(300, self.height))
            self.bottom_rect = pipe_surface.get_rect(midtop=(300, self.height + 150))  # Gap between top and bottom pipe

        def move(self):
            self.top_rect.centerx -= 2
            self.bottom_rect.centerx -= 2

        def reset(self):
            self.height = random.randint(100, 300)
            self.top_rect.midbottom = (300, self.height)
            self.bottom_rect.midtop = (300, self.height + 150)

    # Game Loop
    pipes = []  # List to hold pipes
    pipe_generation_interval = 1500  # Time in milliseconds between pipe generations
    last_pipe_time = pygame.time.get_ticks()  # Time of last pipe creation

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 6  # Bird goes up when space is pressed
                if event.key == pygame.K_SPACE and not game_active:
                    game_active = True
                    pipes = []  # Reset pipes
                    bird_rect.centery = 256
                    bird_movement = 0
                    score = 0

        screen.blit(bg_surface, (0, 0))

        if game_active:
            # Bird
            bird_movement += gravity
            bird_rect.centery += bird_movement
            screen.blit(bird_surface, bird_rect)

            # Pipe generation and movement
            current_time = pygame.time.get_ticks()

            # Generate a new pipe at regular intervals
            if current_time - last_pipe_time >= pipe_generation_interval:
                pipes.append(Pipe())  # Add a new pipe
                last_pipe_time = current_time  # Update last pipe generation time

            # Move pipes
            for pipe in pipes:
                pipe.move()
                screen.blit(pipe_surface, pipe.top_rect)
                screen.blit(pipe_surface, pipe.bottom_rect)

                # Remove pipes that are off-screen
                if pipe.top_rect.right < 0:
                    pipes.remove(pipe)
                    score += 1  # Increase score when passing a pipe

            # Collision
            for pipe in pipes:
                if bird_rect.colliderect(pipe.top_rect) or bird_rect.colliderect(pipe.bottom_rect):
                    game_active = False
            if bird_rect.top <= -100 or bird_rect.bottom >= 480:
                game_active = False

            # Score
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(text, (144 - text.get_width() // 2, 50))

        # Game Over
        else:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Game Over', True, (255, 255, 255))
            screen.blit(text, (75, 200))
            text = font.render('Press Space to restart', True, (255, 255, 255))
            screen.blit(text, (20, 250))

        # Floor
        floor_x_pos -= 1
        screen.blit(floor_surface, (floor_x_pos, floor_y_pos))
        screen.blit(floor_surface, (floor_x_pos + 288, floor_y_pos))  # Repeat floor for scrolling effect
        if floor_x_pos <= -288:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(120)

flappy_bird()
