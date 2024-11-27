import pygame
import random
from collections import deque
import os  
import math 

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SPEED = 5
DELAY_FRAMES = 30  # Delay for the clone in frames
BLOCK_SIZE = 35
PLAYER_SIZE = 50
MINIMUM_DISTANCE = 250  # Minimum distance between player and randomly spawned enemies


# Colors
PLAYER_COLOR = (0, 255, 0)
CLONE_COLOR = (255, 0, 0)
BLOCK_COLOR = (255, 255, 100)
BACKGROUND_COLOR = (15, 15, 15)
TEXT_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("THE PAST CONSUMES..")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 48)

# Load assets
assets_folder = os.path.join(os.getcwd(), "assets")
background_image = pygame.image.load(os.path.join(assets_folder, "background.jpg"))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_character = pygame.image.load(os.path.join(assets_folder, "playerCharacter.png"))
player_character = pygame.transform.scale(player_character, (PLAYER_SIZE, PLAYER_SIZE))
clone_character = pygame.image.load(os.path.join(assets_folder, "cloneCharacter.png"))
clone_character = pygame.transform.scale(clone_character, (PLAYER_SIZE, PLAYER_SIZE))
coin_image = pygame.image.load(os.path.join(assets_folder, "coin.png"))
coin_image = pygame.transform.scale(coin_image, (BLOCK_SIZE, BLOCK_SIZE))  
enemy_image = pygame.image.load(os.path.join(assets_folder, "mushroom.png"))
enemy_image = pygame.transform.scale(enemy_image, (PLAYER_SIZE, PLAYER_SIZE))
pause_button_normal = pygame.image.load(os.path.join(assets_folder, "pauseButtonNormal.webp"))
pause_button_normal = pygame.transform.scale(pause_button_normal, (PLAYER_SIZE, PLAYER_SIZE))
pause_button_hover = pygame.image.load(os.path.join(assets_folder, "pauseButtonHover.png"))
pause_button_hover = pygame.transform.scale(pause_button_hover, (PLAYER_SIZE, PLAYER_SIZE))

# Load Audio assets
background_music = pygame.mixer.Sound('assets/backgroundMusic.mp3')
background_music.set_volume(0.6)
coin_sound = pygame.mixer.Sound('assets/coinSound.mp3')
coin_sound.set_volume(0.5)
death_sound = pygame.mixer.Sound('assets/deathSound.mp3')
death_sound.set_volume(1)
victory_sound = pygame.mixer.Sound('assets/victorySound.mp3')
victory_sound.set_volume(1)

# Enemy Initialization
enemies = []

def restart_game():
    global player_pos, clone_positions, block_pos, score, game_over, clone_active, enemies
    player_pos = [100, 100]
    clone_positions = deque(maxlen=DELAY_FRAMES)
    block_pos = [random.randint(0, SCREEN_WIDTH - BLOCK_SIZE), random.randint(0, SCREEN_HEIGHT - BLOCK_SIZE)]
    score = 0
    game_over = False
    clone_active = False
    enemies = []

# Function to calculate the distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def spawn_enemy():
    # Initialize enemy position
    enemy = {}

    # Spawn enemy at a random position, making sure it's not too close to the player
    while True:
        enemy_pos = [
            random.randint(0, SCREEN_WIDTH - PLAYER_SIZE),
            random.randint(0, SCREEN_HEIGHT - PLAYER_SIZE),
        ]
        # Check if the spawn position is far enough from the player
        if distance(player_pos, enemy_pos) > MINIMUM_DISTANCE:
            enemy["pos"] = enemy_pos
            break  # Exit the loop once a valid spawn position is found

    # Set random speed for the enemy
    enemy["speed"] = [random.choice([-3, 3]), random.choice([-3, 3])]  # Random x and y speed

    # Add the enemy to the list
    enemies.append(enemy)

# Initialize game state
state = "menu"  # choose from various states!!
restart_game()

# Game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key presses based on game state
        if state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Start game
                    state = "playing"
                elif event.key == pygame.K_e:  # Exit game
                    running = False
        elif state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()
                state = "playing"
        elif state == "win":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()
                state = "playing"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                restart_game()
                state = "menu"

    if state == "menu":
        # Main menu screen with background image
        screen.blit(background_image, (0, 0))

        # Main menu background music
        background_music.play()

        title_text = font.render("THE PAST CONSUMES", True, (150, 50, 50))
        play_text = font.render("PLAY!", True, TEXT_COLOR)
        exit_text = font.render("EXIT.", True, TEXT_COLOR)

        # Adjust button size
        button_width = max(play_text.get_width(), exit_text.get_width()) + 120  # Add padding for larger buttons
        button_height = 60  # Make buttons taller
        button_gap = 80  # Space between the buttons

        # Create button rectangles with more space
        play_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - 100, button_width, button_height
        )
        exit_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_gap - 100, button_width, button_height
        )

        # Detect mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()

        # Hover effect: Check if the mouse is over the button and change color
        if play_button_rect.collidepoint(mouse_pos):
            play_color = (200, 150, 150)  # Lighter color for hover effect
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                background_music.stop()
                state = "playing"
        else:
            play_color = (200, 50, 50)  # Normal color for play button

        if exit_button_rect.collidepoint(mouse_pos):
            exit_color = (200, 150, 150)  # Lighter color for hover effect
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                running = False
        else:
            exit_color = (200, 50, 50)  # Normal color for exit button

        # Draw buttons with hover effect
        pygame.draw.rect(screen, play_color, play_button_rect)
        pygame.draw.rect(screen, exit_color, exit_button_rect)

        # Draw the text on buttons
        screen.blit(play_text, (play_button_rect.x + (button_width - play_text.get_width()) // 2, play_button_rect.y + (button_height - play_text.get_height()) // 2))
        screen.blit(exit_text, (exit_button_rect.x + (button_width - exit_text.get_width()) // 2, exit_button_rect.y + (button_height - exit_text.get_height()) // 2))

        # Draw title text
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 200))

        # Handle keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Start game
                background_music.stop()
                state = "playing"
            elif event.key == pygame.K_e:  # Exit game
                running = False

    elif state == "playing" and not game_over:
        # Enemy activation logic: spawn a new enemy every 5 points
        if score > 0 and score % 5 == 0 and len(enemies) < score // 5:
            spawn_enemy()
       
        # Win state logic 
        if score >= 25:
            victory_sound.play()
            # Pulsing "YOU WIN!" text
            colors = [(0, 255, 0), (0, 0, 0)]
            
            for i in range(5):
                for color in colors:
                    screen.blit(font.render("YOU WIN!", True, color), (300, 275))
                    pygame.display.update()
                    pygame.time.wait(250)
        
            state = "win"

        # Move and render all enemies
        for enemy in enemies:
            # Move the enemy
            enemy["pos"][0] += enemy["speed"][0]
            enemy["pos"][1] += enemy["speed"][1]

            # Bounce enemy off the screen edges
            if enemy["pos"][0] <= 0 or enemy["pos"][0] >= SCREEN_WIDTH - PLAYER_SIZE:
                enemy["speed"][0] = -enemy["speed"][0]
            if enemy["pos"][1] <= 0 or enemy["pos"][1] >= SCREEN_HEIGHT - PLAYER_SIZE:
                enemy["speed"][1] = -enemy["speed"][1]

            # Draw the enemy
            screen.blit(enemy_image, (enemy["pos"][0], enemy["pos"][1]))

            # Check for collision with the enemy
            if (
                player_pos[0] < enemy["pos"][0] + PLAYER_SIZE
                and player_pos[0] + PLAYER_SIZE > enemy["pos"][0]
                and player_pos[1] < enemy["pos"][1] + PLAYER_SIZE
                and player_pos[1] + PLAYER_SIZE > enemy["pos"][1]
            ):
                game_over = True
                death_sound.play()
                
                # Pulsing "YOU LOSE!" text
                colors = [(255, 0, 0), (0, 0, 0)]
                
                for i in range(5):
                    for color in colors:
                        screen.blit(font.render("YOU LOSE!", True, color), (300, 275))
                        pygame.display.update()
                        pygame.time.wait(250)
                state = "game_over"

        # Player movement
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] | keys[pygame.K_UP]):
            player_pos[1] -= PLAYER_SPEED
            clone_active = True  # Activate clone movement
        if (keys[pygame.K_s] | keys[pygame.K_DOWN]):
            player_pos[1] += PLAYER_SPEED
            clone_active = True
        if (keys[pygame.K_a] | keys[pygame.K_LEFT]):
            player_pos[0] -= PLAYER_SPEED
            clone_active = True
        if (keys[pygame.K_d] | keys[pygame.K_RIGHT]):
            player_pos[0] += PLAYER_SPEED
            clone_active = True

        # Constrain player within screen bounds
        player_pos[0] = max(0, min(SCREEN_WIDTH - PLAYER_SIZE, player_pos[0]))
        player_pos[1] = max(0, min(SCREEN_HEIGHT - PLAYER_SIZE, player_pos[1]))

        # Save player position to clone's history
        if clone_active:
            clone_positions.append(tuple(player_pos))

        # Move the clone if enough frames have passed
        if len(clone_positions) == DELAY_FRAMES:
            clone_pos = clone_positions[0]
            # Draw the clone using its image
            screen.blit(clone_character, (clone_pos[0], clone_pos[1]))

            # Check for collision with the clone
            if (
                player_pos[0] < clone_pos[0] + PLAYER_SIZE
                and player_pos[0] + PLAYER_SIZE > clone_pos[0]
                and player_pos[1] < clone_pos[1] + PLAYER_SIZE
                and player_pos[1] + PLAYER_SIZE > clone_pos[1]
            ):
                game_over = True
                death_sound.play()

                # Pulsing "YOU LOSE!" text
                colors = [(255, 0, 0), (0, 0, 0)]

                for i in range(5):
                    for color in colors:
                        screen.blit(font.render("YOU LOSE!", True, color), (300, 275))
                        pygame.display.update()
                        pygame.time.wait(250)
                state = "game_over"


        # Define the button position
        button_pos = (745, 5)
        BUTTON_WIDTH, BUTTON_HEIGHT = pause_button_normal.get_width(), pause_button_normal.get_height()

        # Check for mouse hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (
            button_pos[0] <= mouse_x <= button_pos[0] + BUTTON_WIDTH
            and button_pos[1] <= mouse_y <= button_pos[1] + BUTTON_HEIGHT
        ):
            # Draw the hover image
            screen.blit(pause_button_hover, button_pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                state = "paused"  # Change state to paused
        else:
            # Draw the normal image
            screen.blit(pause_button_normal, button_pos)
        # Draw player using the image
        screen.blit(player_character, (player_pos[0], player_pos[1]))

        # Draw block
        screen.blit(coin_image, (block_pos[0], block_pos[1]))

        # Check for collision with coin 
        if (
            player_pos[0] < block_pos[0] + BLOCK_SIZE
            and player_pos[0] + PLAYER_SIZE > block_pos[0]
            and player_pos[1] < block_pos[1] + BLOCK_SIZE
            and player_pos[1] + PLAYER_SIZE > block_pos[1]
        ):
            # Update score and respawn coin
            coin_sound.play()
            score += 1
            block_pos = [
                random.randint(0, SCREEN_WIDTH - BLOCK_SIZE),
                random.randint(0, SCREEN_HEIGHT - BLOCK_SIZE),
            ]

        # Render score
        score_text = font.render(f"Score: {score}", True, (230, 0, 0))
        screen.blit(score_text, (10, 10))
    
    elif state == "paused":
        # Background dim effect
        dim_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dim_overlay.set_alpha(180)  # Transparency
        dim_overlay.fill((0, 0, 0))  # Black overlay
        screen.blit(dim_overlay, (0, 0))

        # Render Pause Menu Text
        paused_text = font.render("Paused", True, TEXT_COLOR)
        screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - 200))

        # Define button dimensions
        button_width, button_height = 200, 60
        button_gap = 80

        # Resume Button
        resume_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - 50, button_width, button_height
        )
        exit_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_gap, button_width, button_height
        )

        # Detect mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Resume Button Hover Effect
        if resume_button_rect.collidepoint(mouse_pos):
            resume_color = (150, 150, 255)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                state = "playing"  # Resume game
        else:
            resume_color = (100, 100, 255)

        # Exit Button Hover Effect
        if exit_button_rect.collidepoint(mouse_pos):
            exit_color = (255, 150, 150)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                state = "menu" # Go back to menu page
        else:
            exit_color = (255, 100, 100)

        # Draw Buttons
        pygame.draw.rect(screen, resume_color, resume_button_rect)
        pygame.draw.rect(screen, exit_color, exit_button_rect)

        # Add Text to Buttons
        resume_text = font.render("Resume", True, TEXT_COLOR)
        exit_text = font.render("Exit", True, TEXT_COLOR)
        screen.blit(resume_text, (resume_button_rect.x + (button_width - resume_text.get_width()) // 2,
                                resume_button_rect.y + (button_height - resume_text.get_height()) // 2))
        screen.blit(exit_text, (exit_button_rect.x + (button_width - exit_text.get_width()) // 2,
                                exit_button_rect.y + (button_height - exit_text.get_height()) // 2))

    elif state == "game_over":
        # background image
        screen.blit(background_image, (0, 0))
        
        button_height = 60  # Make buttons taller
        button_width = max(play_text.get_width(), exit_text.get_width()) + 220 # max width of button based on window size
        
        # Game Over screen
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        play_again_text = font.render("Click to Restart", True, TEXT_COLOR)

        # Create button rectangles 
        play_again_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - 100, button_width, button_height
        )
        exit_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2, button_width, button_height
        )

        # Detect mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()

        # Hover effect: Check if the mouse is over the button and change color
        if play_again_rect.collidepoint(mouse_pos):
            play_color = (200, 150, 150)  # Lighter color for hover effect
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                restart_game()
                state = "playing"
        else:
            play_color = (200, 50, 50)  # Normal color for play button
        # Exit Button Hover Effect
        if exit_button_rect.collidepoint(mouse_pos):
            exit_color = (200, 150, 150)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                state = "menu" # Go back to menu page
        else:
            exit_color = (200, 50, 50)

        # draw the play again button
        pygame.draw.rect(screen, play_color, play_again_rect)
        pygame.draw.rect(screen, exit_color, exit_button_rect)

        # Draw the text on buttons
        screen.blit(play_again_text, (play_again_rect.x + (button_width - play_again_text.get_width()) // 2, play_again_rect.y + (button_height - play_again_text.get_height()) // 2))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 250))
        screen.blit(exit_text, (exit_button_rect.x + (button_width - exit_text.get_width()) // 2, exit_button_rect.y + (button_height - exit_text.get_height()) // 2))
        
    elif state == "win":
        # Background image
        screen.blit(background_image, (0, 0))

        # Win screen text
        win_text = font.render("Congratulations! You Won!", True, (0, 255, 0))
        play_again_text = font.render("Press R to Restart", True, TEXT_COLOR)

        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
