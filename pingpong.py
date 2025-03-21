import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 15

# Paddle positions
left_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball position and velocity
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x, ball_speed_y = 4, 4

# Paddle speed
paddle_speed = 6

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Scores
left_score = 0
right_score = 0

# Hardcore mode variables
hardcore_mode = False
ball_touches = 0
obstacle = None
red_blocks = []

# Font for displaying scores and buttons
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Home screen with buttons
def home_screen():
    global hardcore_mode
    screen.fill(BLACK)

    # Button dimensions
    button_width, button_height = 300, 60
    singleplayer_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 150, button_width, button_height)
    multiplayer_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 50, button_width, button_height)
    hardcore_toggle_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 50, button_width, button_height)
    how_to_play_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 150, button_width, button_height)

    # Draw buttons
    pygame.draw.rect(screen, GRAY, singleplayer_button)
    pygame.draw.rect(screen, GRAY, multiplayer_button)
    pygame.draw.rect(screen, GRAY, hardcore_toggle_button)
    pygame.draw.rect(screen, GRAY, how_to_play_button)

    # Button text
    singleplayer_text = button_font.render("Singleplayer", True, WHITE)
    multiplayer_text = button_font.render("Multiplayer", True, WHITE)
    hardcore_toggle_text = button_font.render(f"Hardcore: {'ON' if hardcore_mode else 'OFF'}", True, WHITE)
    how_to_play_text = button_font.render("How to Play", True, WHITE)

    screen.blit(singleplayer_text, (singleplayer_button.x + 50, singleplayer_button.y + 10))
    screen.blit(multiplayer_text, (multiplayer_button.x + 50, multiplayer_button.y + 10))
    screen.blit(hardcore_toggle_text, (hardcore_toggle_button.x + 50, hardcore_toggle_button.y + 10))
    screen.blit(how_to_play_text, (how_to_play_button.x + 50, how_to_play_button.y + 10))

    pygame.display.flip()

    # Wait for button click
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if singleplayer_button.collidepoint(mouse_pos):
                    return "singleplayer"
                elif multiplayer_button.collidepoint(mouse_pos):
                    return "multiplayer"
                elif hardcore_toggle_button.collidepoint(mouse_pos):
                    hardcore_mode = not hardcore_mode
                    return home_screen()
                elif how_to_play_button.collidepoint(mouse_pos):
                    show_how_to_play()

# Show "How to Play" screen
def show_how_to_play():
    screen.fill(BLACK)
    instructions = [
        "How to Play:",
        "1. Use W/S to move the left paddle.",
        "2. Use UP/DOWN to move the right paddle.",
        "3. In Singleplayer, the AI controls the right paddle.",
        "4. Score by making the ball pass the opponent's paddle.",
        "Hardcore Mode:",
        "- Adds obstacles and random challenges.",
        "Press any key to return to the main menu."
    ]

    y_offset = HEIGHT // 4
    for line in instructions:
        text = button_font.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 50

    pygame.display.flip()

    # Wait for any key press
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

# AI for singleplayer mode
def ai_move():
    if ball.centery > right_paddle.centery + PADDLE_HEIGHT // 4:
        right_paddle.y += paddle_speed
    elif ball.centery < right_paddle.centery - PADDLE_HEIGHT // 4:
        right_paddle.y -= paddle_speed

    # Prevent the paddle from going out of bounds
    if right_paddle.top < 0:
        right_paddle.top = 0
    if right_paddle.bottom > HEIGHT:
        right_paddle.bottom = HEIGHT

# Add obstacle after 10 ball touches
def add_obstacle():
    global obstacle
    obstacle = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 20)

# Add red blocks after 30 ball touches
def add_red_blocks():
    global red_blocks
    red_blocks = [
        pygame.Rect(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 20, 20),
        pygame.Rect(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 20, 20)
    ]

# Check for collision with red blocks
def check_red_block_collision():
    for block in red_blocks:
        if ball.colliderect(block):
            return True
    return False

# Main game loop
while True:
    # Show home screen and get selected game mode
    game_mode = home_screen()

    # Reset variables for hardcore mode
    ball_touches = 0
    obstacle = None
    red_blocks = []

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed

        if game_mode == "multiplayer":
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= paddle_speed
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += paddle_speed
        elif game_mode == "singleplayer":
            ai_move()

        # Ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Ball collision with paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1
            ball_touches += 1

        # Hardcore mode logic
        if hardcore_mode:
            if ball_touches == 10 and not obstacle:
                add_obstacle()
            if ball_touches == 20:
                # Randomize paddle speed
                paddle_speed = random.choice([3, 10])  # Randomly set to slow or fast
            if ball_touches == 30 and not red_blocks:
                add_red_blocks()
            if ball_touches >= 40:
                # Display "YOU WON" screen
                screen.fill(BLACK)
                win_text = font.render("YOU WON!", True, WHITE)
                email_text = button_font.render("Email recording to ivaansri.contact@gmail.com", True, WHITE)
                screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))
                screen.blit(email_text, (WIDTH // 2 - email_text.get_width() // 2, HEIGHT // 2 + 50))
                pygame.display.flip()
                pygame.time.wait(5000)
                pygame.quit()
                sys.exit()

            # Check for red block collision
            if check_red_block_collision():
                # Player loses in Hardcore Mode
                screen.fill(BLACK)
                ded_text = font.render("YOUR DED", True, RED)
                screen.blit(ded_text, (WIDTH // 2 - ded_text.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()

        # Ball collision with obstacle
        if obstacle and ball.colliderect(obstacle):
            ball_speed_y *= -1

        # Ball out of bounds
        if ball.left <= 0 or ball.right >= WIDTH:
            if hardcore_mode:
                # Player loses in Hardcore Mode
                screen.fill(BLACK)
                ded_text = font.render("YOUR DED", True, RED)
                screen.blit(ded_text, (WIDTH // 2 - ded_text.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()
            else:
                # Normal mode scoring
                if ball.left <= 0:
                    right_score += 1
                if ball.right >= WIDTH:
                    left_score += 1
                ball.x, ball.y = WIDTH // 2, HEIGHT // 2
                ball_speed_x *= -1

        # Drawing everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Draw obstacle
        if obstacle:
            pygame.draw.rect(screen, GRAY, obstacle)

        # Draw red blocks
        for block in red_blocks:
            pygame.draw.rect(screen, RED, block)

        # Display scores
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WIDTH // 4, 20))
        screen.blit(right_text, (WIDTH * 3 // 4, 20))

        # Update display
        pygame.display.flip()

        # Frame rate
        clock.tick(60)