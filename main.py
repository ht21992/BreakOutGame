import pygame
import random
import math
from paddle import Paddle
from ball import Ball
from brick import Brick
from menu import Menu
import imageio
import threading

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (150, 75, 0)
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
BRICK_ROWS = 5
BRICK_COLS = 10
FONT_SIZE = 24
COLORS_HITS = {"RED": 5, "GREEN": 2, "YELLOW": 3, "BLUE": 4, "WHITE": 1}
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Buster")
font = pygame.font.Font(None, FONT_SIZE)

clock = pygame.time.Clock()


# Load the GIF using imageio
gif_path = "./images/bg.gif"
gif = imageio.mimread(gif_path)

# Convert the frames to Pygame surfaces and resize them
resized_frames = []
for frame in gif:
    surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    resized_frame = pygame.transform.scale(surface, (WIDTH, HEIGHT))
    resized_frames.append(resized_frame)

# Function to update the GIF animation
def update_gif():
    global frame_index
    while True:
        # Delay between frames to make the gif runs slower
        pygame.time.delay(100)
        frame_index = (frame_index + 1) % len(resized_frames)


# Create and start a thread for updating the GIF animation
gif_thread = threading.Thread(target=update_gif, daemon=True)
gif_thread.start()

def load_background_music():
    global current_track
    # Load background music and soundeffects
    track_range = list(range(1,6))
    track_range.remove(current_track)

    current_track = random.choice(track_range)

    pygame.mixer.music.load(f'./audio/themes/SoundTrack{current_track}.mp3')
    # Set volume
    pygame.mixer.music.set_volume(0.5)

    # Start playing the background music
    pygame.mixer.music.play(-1)  # Loop the music indefinitely


brick_hit_sound = pygame.mixer.Sound('./audio/effects/hit.mp3')

def reset_game():
    global score, lives
    score = 0
    lives = 3
    all_sprites.empty()
    bricks.empty()
    paddle.rect.center = (WIDTH // 2, HEIGHT - 50)
    all_sprites.add(paddle)

    # Create a new white ball
    ball = Ball()
    ball.color = (255, 255, 255)  # Reset ball's color to white
    ball.rect.center = (WIDTH // 2, HEIGHT // 2)  # Set initial position
    balls_sprite.add(ball)
    all_sprites.add(ball)  # Add the ball to all_sprites group

    # Remove all brown balls
    for brown_ball in balls_sprite.sprites():
        if brown_ball.color == BROWN:
            brown_ball.kill()

    # Create bricks
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            color = random.choice(list(COLORS_HITS.keys()))
            hits = COLORS_HITS[color]
            brick = Brick(
                col * (BRICK_WIDTH + 2),
                row * (BRICK_HEIGHT + 2),
                color,
                hits,
                all_sprites,
            )
            bricks.add(brick)
            all_sprites.add(brick)


# Create sprites
gray_balls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
drop_boxes = pygame.sprite.Group()

paddle = Paddle()
balls_sprite = pygame.sprite.Group()

for _ in range(1):
    ball = Ball()
    balls_sprite.add(ball)
    all_sprites.add(ball)

all_sprites.add(paddle)

# Create bricks
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        color = random.choice(list(COLORS_HITS.keys()))
        hits = COLORS_HITS[color]
        brick = Brick(
            col * (BRICK_WIDTH + 2), row * (BRICK_HEIGHT + 2), color, hits, all_sprites
        )
        bricks.add(brick)
        all_sprites.add(brick)


def draw_catch_text(text):
    catch_text_surface = font.render(text, True, WHITE)
    catch_text_rect = catch_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(catch_text_surface, catch_text_rect)


# Text variables
catch_text = ""
catch_text_timer = 0

# Game variables
score = 0
lives = 3
current_track = 1
game_over = False
new_game = False
dizziness_mode = False


# Game loop
running = True
in_main_menu = True
paused = False  # variable to track whether the game is paused
countdown = 0  # Countdown variable

load_background_music()

# Main menu setup
main_menu = Menu(screen, WIDTH, HEIGHT)

frame_index = 0

while running:

    current_time = pygame.time.get_ticks()

    if in_main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_clicked = main_menu.handle_event(event)
                if button_clicked == "start":
                    in_main_menu = False
                elif button_clicked == "exit":
                    running = False

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle.speed = 8 if dizziness_mode else -8
                elif event.key == pygame.K_RIGHT:
                    paddle.speed = -8 if dizziness_mode else 8
                elif event.key == pygame.K_r and game_over:
                    reset_game()
                    game_over = False
                elif event.key == pygame.K_c:
                    load_background_music()
                elif event.key == pygame.K_m:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    paddle.speed = 0
            elif event.type == pygame.MOUSEMOTION:
                # Move paddle with mouse movement
                if not dizziness_mode:
                    paddle.rect.centerx = event.pos[0]
                else:
                    # In dizziness mode, paddle moves inversely proportional to mouse movement
                    paddle.rect.centerx += (WIDTH / 2 - event.pos[0]) // 20

                # Ensure paddle stays within the screen bounds
                if paddle.rect.left < 0:
                    paddle.rect.left = 0
                elif paddle.rect.right > WIDTH:
                    paddle.rect.right = WIDTH



        if not paused:  # Update and draw the game only if it's not paused
            if not game_over:

                # Countdown
                if countdown > 0:

                    count_text = font.render(str(math.ceil(countdown / 60)), True, WHITE)
                    count_rect = count_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    screen.blit(count_text, count_rect)
                    countdown -= 1

                else:
                    all_sprites.update()

                # Check for collisions for each ball
                for ball in balls_sprite:
                    hits = pygame.sprite.spritecollide(ball, bricks, False)
                    for brick in hits:
                        score = brick.hit(score, ball, drop_boxes)
                        ball.speed_y *= -1
                        brick_hit_sound.play()  # Play the brick hit sound effect

                    dropBoxCatch = pygame.sprite.spritecollide(paddle, drop_boxes, False)
                    for drop_box in dropBoxCatch:
                        FPS, dizziness_mode, lives, msg = drop_box.catch(
                            paddle, FPS, dizziness_mode, lives, balls_sprite, all_sprites
                        )
                        catch_text = msg
                        catch_text_timer = current_time  # Reset timer

                    # Check collision with paddle
                    if pygame.sprite.collide_rect(ball, paddle):
                        ball.speed_y *= -1
                        offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
                        angle = offset * math.pi / 3
                        ball.speed_x = 5 * math.sin(angle)
                        ball.speed_y = -5 * math.cos(angle)

                    # Game over
                    if ball.rect.bottom >= HEIGHT and ball.color != BROWN:
                        for brown_ball in balls_sprite.sprites():
                            if brown_ball.color == BROWN:
                                brown_ball.kill()
                        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
                        ball.speed_y = -5
                        lives -= 1
                        countdown = 30  # Start the countdown for 0.5 seconds (30 frames)
                        FPS = 60
                        dizziness_mode = False
                        catch_text = ""
                        paddle.image = paddle.original_image

                        if lives <= 0:
                            game_over = True

                    # Win condition
                    if len(bricks) == 0:
                        game_over = True
                        new_game = True


            # Display the current frame of the GIF as the background
            screen.blit(resized_frames[frame_index], (0, 0))
            all_sprites.draw(screen)

            # Draw score and lives with background
            score_text = font.render(f"Score: {score}", True, WHITE)
            score_rect = score_text.get_rect(top=20, left=20)
            pygame.draw.rect(screen, BLACK, score_rect)
            screen.blit(score_text, score_rect)

            lives_text = font.render(f"Lives: {lives}", True, WHITE)
            lives_rect = lives_text.get_rect(top=20, right=WIDTH - 20)
            pygame.draw.rect(screen, BLACK, lives_rect)
            screen.blit(lives_text, lives_rect)

            # Draw catch text if applicable
            if catch_text:
                draw_catch_text(catch_text)
                if current_time - catch_text_timer >= 5000:  # 5000 milliseconds = 5 seconds
                    catch_text = ""  # Clear catch text after 5 seconds

            # Game Over
            if game_over:
                bg_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)
                pygame.draw.rect(screen, BLACK, bg_rect)
                if lives <= 0:
                    game_over_text = font.render("Game Over", True, WHITE)
                else:
                    game_over_text = font.render("You Win!", True, WHITE)
                game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                restart_text = font.render("Press 'R' to restart", True, WHITE)
                restart_rect = restart_text.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2 + FONT_SIZE)
                )
                screen.blit(game_over_text, game_over_rect)
                screen.blit(restart_text, restart_rect)

        # Game is paused
        if paused:
            # Draw black background box
            pause_box = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 2)
            pygame.draw.rect(screen, BLACK, pause_box)

            # Draw white text "Game is paused"
            pause_text = font.render("Game is paused", True, WHITE)
            pause_text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(pause_text, pause_text_rect)


    if in_main_menu:
        main_menu.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
