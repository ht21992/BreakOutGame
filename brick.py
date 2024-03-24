import pygame
from particle import Particle
import math
from dropBox import dropBox

BRICK_WIDTH, BRICK_HEIGHT = 80, 30
BORDER_WIDTH = 1

COLORS = {"RED":(255, 0, 0),"GREEN":(0, 255, 0), "BLUE":(0, 0, 255), "WHITE":(255, 255, 255), "YELLOW":(255, 255, 0)}

BRICKS_COLORS = {"RED":{"score":50, "lower_color":"BLUE"},
                 "BLUE":{"score":40, "lower_color":"YELLOW"},
                 "YELLOW":{"score":30, "lower_color":"GREEN"},
                 "GREEN":{"score":20, "lower_color":"WHITE"},}

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color, hits,all_sprites):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.color = color
        self.hits = hits
        self.update_color()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.all_sprites = all_sprites

    def update_color(self):
        self.image.fill(COLORS[self.color])
        pygame.draw.rect(self.image, (255, 255, 255), self.image.get_rect(), BORDER_WIDTH)  # Draw border

    def calculate_angle_reflection(self,ball):
        # Calculate angle of reflection based on where the ball hits the brick
        offset = (ball.rect.centerx - self.rect.centerx) / (self.rect.width / 2)
        angle = offset * math.pi / 3  # Maximum reflection angle is 60 degrees
        ball.speed_x = 5 * math.sin(angle)
        ball.speed_y = -5 * math.cos(angle)

    def hit(self, score, ball, drop_boxes):
        particles = pygame.sprite.Group()  # Create a sprite group for particles
        for _ in range(10):  # Spawn 10 partials
            particle = Particle(self.rect.centerx, self.rect.centery, COLORS[self.color])
            particles.add(particle)
            self.all_sprites.add(particle)
        self.calculate_angle_reflection(ball)

        if self.color != "WHITE":
            drop_box = dropBox(self.rect.centerx, self.rect.centery,COLORS[self.color])
            drop_boxes.add(drop_box)
            self.all_sprites.add(drop_box)
            new_color = BRICKS_COLORS.get(self.color)
            score += new_color['score']
            self.color = new_color['lower_color']
            self.hits -= 1
            self.update_color()
            drop_box.update()
        else:
            score += 10
            self.kill()
        return score
