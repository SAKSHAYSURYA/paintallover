import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 20  # Size of each grid cell
TEXT_AREA_HEIGHT = 50  # Height of the text area at the top
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600 + TEXT_AREA_HEIGHT  # Ensure the grid area is a perfect multiple of the grid size
GAME_TIME = 60   # Game time in seconds
MOVE_SPEED = 4  # Increase move speed

# Colors
BG_COLOR = (240, 240, 240)  # Light grey background color
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)  # Soft yellow for player border
WHITE = (255, 255, 255)

# Initialize game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Paint Allover')

# Initialize fonts
timer_font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 48)
button_font = pygame.font.Font(None, 60)

# Initialize game variables
player1_color = RED
player2_color = BLUE
game_running = True
game_over = False
clock = pygame.time.Clock()

# Grid data
grid_width = WINDOW_WIDTH // GRID_SIZE
grid_height = (WINDOW_HEIGHT - TEXT_AREA_HEIGHT) // GRID_SIZE
grid = [[None for _ in range(grid_width)] for _ in range(grid_height)]

# Player starting positions
player1_x, player1_y = 0, TEXT_AREA_HEIGHT  # Top left corner (start below text area)
player2_x, player2_y = (grid_width - 1) * GRID_SIZE, (grid_height - 1) * GRID_SIZE + TEXT_AREA_HEIGHT  # Bottom right corner

# Player names
player1_name = ""
player2_name = ""
active_input = None

# Input boxes
input_box1 = pygame.Rect(WINDOW_WIDTH // 4 - 100, WINDOW_HEIGHT // 2 - 50, 200, 50)
input_box2 = pygame.Rect(WINDOW_WIDTH * 3 // 4 - 100, WINDOW_HEIGHT // 2 - 50, 200, 50)
start_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, 200, 50)

# Function to draw text on screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Start screen
start_screen = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if start_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active_input = "player1"
                elif input_box2.collidepoint(event.pos):
                    active_input = "player2"
                elif start_button.collidepoint(event.pos):
                    if player1_name and player2_name:
                        start_screen = False
                        start_time = pygame.time.get_ticks()
                else:
                    active_input = None
            if event.type == pygame.KEYDOWN:
                if active_input == "player1":
                    if event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    else:
                        player1_name += event.unicode
                elif active_input == "player2":
                    if event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    else:
                        player2_name += event.unicode

    if start_screen:
        window.fill(BG_COLOR)
        draw_text("Enter Player Names", input_font, BLACK, window, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        draw_text("Player 1:", input_font, BLACK, window, WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2 - 100)
        draw_text("Player 2:", input_font, BLACK, window, WINDOW_WIDTH * 3 // 4, WINDOW_HEIGHT // 2 - 100)
        
        # Render player names
        pygame.draw.rect(window, WHITE, input_box1)
        pygame.draw.rect(window, WHITE, input_box2)
        pygame.draw.rect(window, YELLOW, start_button)
        draw_text(player1_name, input_font, BLACK, window, input_box1.centerx, input_box1.centery)
        draw_text(player2_name, input_font, BLACK, window, input_box2.centerx, input_box2.centery)
        draw_text("Start", button_font, BLACK, window, start_button.centerx, start_button.centery)
        
        pygame.display.flip()
    else:
        # Calculate elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        if not game_over:
            # Player 1 controls (WASD)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player1_y > TEXT_AREA_HEIGHT:
                player1_y -= MOVE_SPEED
            elif keys[pygame.K_s] and player1_y < WINDOW_HEIGHT - GRID_SIZE:
                player1_y += MOVE_SPEED
            elif keys[pygame.K_a] and player1_x > 0:
                player1_x -= MOVE_SPEED
            elif keys[pygame.K_d] and player1_x < WINDOW_WIDTH - GRID_SIZE:
                player1_x += MOVE_SPEED

            # Player 2 controls (Arrow keys)
            if keys[pygame.K_UP] and player2_y > TEXT_AREA_HEIGHT:
                player2_y -= MOVE_SPEED
            elif keys[pygame.K_DOWN] and player2_y < WINDOW_HEIGHT - GRID_SIZE:
                player2_y += MOVE_SPEED
            elif keys[pygame.K_LEFT] and player2_x > 0:
                player2_x -= MOVE_SPEED
            elif keys[pygame.K_RIGHT] and player2_x < WINDOW_WIDTH - GRID_SIZE:
                player2_x += MOVE_SPEED

            # Update grid with player colors
            x1 = player1_x // GRID_SIZE
            y1 = (player1_y - TEXT_AREA_HEIGHT) // GRID_SIZE
            x2 = player2_x // GRID_SIZE
            y2 = (player2_y - TEXT_AREA_HEIGHT) // GRID_SIZE

            # Allow players to take over each other's color grid
            if grid[y1][x1] != player1_color:
                grid[y1][x1] = player1_color

            if grid[y2][x2] != player2_color:
                grid[y2][x2] = player2_color

            # Clear screen
            window.fill(BG_COLOR)

            # Draw text area background
            pygame.draw.rect(window, BLACK, (0, 0, WINDOW_WIDTH, TEXT_AREA_HEIGHT))

            # Draw grid cells and trails
            for y, row in enumerate(grid):
                for x, color in enumerate(row):
                    if color is not None:
                        pygame.draw.rect(window, color, (x * GRID_SIZE, y * GRID_SIZE + TEXT_AREA_HEIGHT, GRID_SIZE, GRID_SIZE))

            # Hide grid lines by setting them to the background color
            grid_line_color = BG_COLOR
            for x in range(0, WINDOW_WIDTH, GRID_SIZE):
                pygame.draw.line(window, grid_line_color, (x, TEXT_AREA_HEIGHT), (x, WINDOW_HEIGHT))
            for y in range(TEXT_AREA_HEIGHT, WINDOW_HEIGHT, GRID_SIZE):
                pygame.draw.line(window, grid_line_color, (0, y), (WINDOW_WIDTH, y))

            # Draw player 1 and player 2 with larger border
            border_size = 4  # Size of the border
            pygame.draw.rect(window, YELLOW, (x1 * GRID_SIZE, y1 * GRID_SIZE + TEXT_AREA_HEIGHT, GRID_SIZE, GRID_SIZE), border_size)
            pygame.draw.rect(window, YELLOW, (x2 * GRID_SIZE, y2 * GRID_SIZE + TEXT_AREA_HEIGHT, GRID_SIZE, GRID_SIZE), border_size)

            # Calculate areas covered by players
            player1_area = sum(row.count(player1_color) for row in grid)
            player2_area = sum(row.count(player2_color) for row in grid)

            # Display player areas
            draw_text(f'{player1_name} Area: {player1_area}', timer_font, RED, window, 120, 25)
            draw_text(f'{player2_name} Area: {player2_area}', timer_font, BLUE, window, 680, 25)

            # Display timer
            draw_text(f'Time Left: {max(0, GAME_TIME - elapsed_time)}', timer_font, YELLOW, window, WINDOW_WIDTH // 2, 25)

            # Update display
            pygame.display.flip()

            # Check if game time is up
            if elapsed_time >= GAME_TIME:
                game_over = True
                end_time = pygame.time.get_ticks()

        else:
            # Determine the winner based on total area covered
            total_area_player1 = sum(row.count(player1_color) for row in grid)
            total_area_player2 = sum(row.count(player2_color) for row in grid)
            winner = f"{player1_name} wins" if total_area_player1 > total_area_player2 else f"{player2_name} wins" if total_area_player2 > total_area_player1 else "It's a Draw"

            # Display winner
            window.fill(BG_COLOR)
            draw_text("Game Over!", timer_font, BLACK, window, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
            draw_text(f"{winner} with {max(total_area_player1, total_area_player2)} cells covered.", timer_font, BLACK, window, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
            pygame.display.flip()

            # Wait for a moment before quitting
            if pygame.time.get_ticks() - end_time > 5000:
                game_running = False

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
