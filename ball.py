import pygame
import random
import math

BALL_RADIUS = 10
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 800, 600


class Ball(pygame.sprite.Sprite):
    def __init__(self,color=WHITE):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.image.set_colorkey((0, 0, 0))  # Set black color as transparent
        pygame.draw.circle(self.image, color, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = -5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Collision with walls
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1  # Reverse horizontal direction
            # Ensure the ball doesn't go out of bounds
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right >= WIDTH:
                self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.speed_y *= -1  # Reverse vertical direction
            self.rect.top = 0  # Ensure the ball doesn't go out of bounds