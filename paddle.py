import pygame

PADDLE_WIDTH, PADDLE_HEIGHT = 128, 28
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 800, 600


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the paddle image
        self.original_image = pygame.image.load(f"./images/paddle/paddle_{PADDLE_WIDTH}x{PADDLE_HEIGHT}.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (PADDLE_WIDTH, PADDLE_HEIGHT)) # Scale the image
        self.current_width = PADDLE_WIDTH
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 0

    def update(self):
        # Update position based on speed
        self.rect.x += self.speed

        # Ensure paddle stays within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        # Update collision rectangle
        self.rect = self.image.get_rect(center=self.rect.center)
