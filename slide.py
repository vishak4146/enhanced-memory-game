import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
FPS = 30
BUTTON_SIZE = 150
COLORS = {
    'Red': (255, 0, 0),
    'Green': (0, 255, 0),
    'Blue': (0, 0, 255),
    'Yellow': (255, 255, 0),
    'White': (255, 255, 255),
    'Black': (0, 0, 0)
}
BUTTONS = {
    'Red': (75, 75),
    'Green': (375, 75),
    'Blue': (75, 375),
    'Yellow': (375, 375)
}

# Game settings
score = 0
high_score = 0
level_speed = 1000  # Initial speed in milliseconds

# Setup display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Enhanced Memory Game")
clock = pygame.time.Clock()

# Try to load a font, default to None if error
try:
    font = pygame.font.Font(None, 36)
except IOError:
    print("Warning: Font file not found, using default font.")
    font = None

# Function to draw buttons and the score
def draw_buttons(highlight=None):
    screen.fill(COLORS['Black'])  # Clear screen
    for color, pos in BUTTONS.items():
        pygame.draw.rect(screen, COLORS[color if color != highlight else 'White'], (pos[0], pos[1], BUTTON_SIZE, BUTTON_SIZE))
    if font:
        score_text = font.render(f"Score: {score} High Score: {high_score}", True, COLORS['White'])
        screen.blit(score_text, (10, 10))
    pygame.display.update()

# Function to add to the sequence
def add_to_sequence(sequence):
    sequence.append(random.choice(list(BUTTONS.keys())))
    return sequence

# Function to display the sequence
def display_sequence(sequence):
    for color in sequence:
        draw_buttons(highlight=color)
        pygame.time.wait(level_speed)
        draw_buttons()
        pygame.time.wait(int(level_speed / 2))

# Function to update game speed dynamically
def update_game_speed():
    global level_speed
    level_speed = max(400, level_speed - 30)

# Main game function
def main():
    global score, high_score, level_speed
    running = True
    game_sequence = []
    player_sequence = []
    game_over = False

    while running:
        if game_over:
            draw_buttons()
            over_text = font.render("Game Over! Press Space to restart", True, COLORS['Red']) if font else None
            if over_text:
                screen.blit(over_text, (WINDOW_WIDTH / 2 - over_text.get_width() / 2, WINDOW_HEIGHT / 2))
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_sequence = []
                    player_sequence = []
                    score = 0
                    level_speed = 1000
                    game_sequence = add_to_sequence(game_sequence)
                    display_sequence(game_sequence)
                    game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                for color, pos in BUTTONS.items():
                    if pos[0] <= x <= pos[0] + BUTTON_SIZE and pos[1] <= y <= pos[1] + BUTTON_SIZE:
                        player_sequence.append(color)
                        draw_buttons(highlight=color)
                        pygame.time.wait(500)
                        if len(player_sequence) <= len(game_sequence):
                            # Check each input immediately against the sequence
                            if player_sequence[-1] != game_sequence[len(player_sequence) - 1]:
                                game_over = True
                                draw_buttons()  # Update the display to show no highlights
                                over_text = font.render("Game Over! Press Space to restart", True, COLORS['Red'])
                                screen.blit(over_text, (WINDOW_WIDTH / 2 - over_text.get_width() / 2, WINDOW_HEIGHT / 2))
                                pygame.display.update()
                                break
                        if len(player_sequence) == len(game_sequence) and not game_over:
                            score += 10
                            if score > high_score:
                                high_score = score
                            update_game_speed()
                            player_sequence = []
                            game_sequence = add_to_sequence(game_sequence)
                            display_sequence(game_sequence)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
