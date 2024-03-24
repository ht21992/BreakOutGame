import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((3, 3))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = 20  # partial life

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.life -= 1
        if self.life <= 0:
            self.kill()
