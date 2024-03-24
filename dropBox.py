import pygame
import random
from ball import Ball
from PIL import Image

# Constants
BOX_TYPES = {
    "empty": "Empty Brick",
    "paddle_size": "Paddle Size Changed",
    "speed": "Speed Changed",
    "dizzy":"Dizziness Mode",
    "live":"One Live Granted",
    "ball":"Pseudo Ball Added"
}
BOX_SIZES ={
    "paddle_size": (32,12),
    "speed": (48,48),
    "dizzy":(48,48),
    "live":(48,48),
    "ball":(32,32)}
PADDLE_WIDTH, PADDLE_HEIGHT = 128, 28
BROWN = (150, 75, 0)

class dropBox(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.speed_y = 5
        self.box_type = random.choices(list(BOX_TYPES.keys()), weights=[0.8, 0.3, 0.3,0.3,0.1,0.3])[
            0
        ]  # specify the box type
        if self.box_type != "empty":
            # Colored Drop Box
            # self.image = pygame.Surface((15, 15))
            # self.image.fill(color)
            
            # Image Drop Box
            self.image = pygame.image.load(f"./images/drop_boxes/{self.box_type}.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, BOX_SIZES[self.box_type])
            self.rect = self.image.get_rect(center=(x, y))


    def update(self):
        if self.box_type == "empty":
            self.kill()
        else:
            self.rect.y += self.speed_y
            if (
                self.rect.top > pygame.display.get_surface().get_height()
            ):  # If box is below the screen
                self.kill()  # Remove the box from sprite group

    def update_paddle(self, paddle, new_width):
        current_center = paddle.rect.center  # Get current center position of the paddle
        paddle.original_image = pygame.image.load(f"./images/paddle/paddle_{new_width}x{PADDLE_HEIGHT}.png").convert_alpha()
        paddle.original_image = pygame.transform.scale(paddle.original_image, (PADDLE_WIDTH, PADDLE_HEIGHT))
        paddle.image = pygame.transform.scale(paddle.original_image, (new_width, PADDLE_HEIGHT))
        paddle.rect = paddle.image.get_rect(center=current_center)  # Maintain the center position
        paddle.current_width = new_width

    def catch(self, paddle, fps,dizziness_mode,lives,balls_sprite,all_sprites):
        if self.box_type == "paddle_size":
            paddle_widths_list = [64,96,128,160,192]
            paddle_widths_list.remove(paddle.current_width)
            new_value = random.choice(paddle_widths_list)
            self.update_paddle(paddle, new_value)
        elif self.box_type == "speed":
            fps_choices = [45, 60, 120]
            fps_choices.remove(fps)
            new_value = random.choice(fps_choices)
            fps = new_value
        elif self.box_type == "dizzy":
            dizziness_mode = not dizziness_mode
            BOX_TYPES[self.box_type] = "Dizziness Mode" if dizziness_mode else "Dizziness Treated"
        elif self.box_type == "cure":
            dizziness_mode = False
        elif self.box_type == "live":
            lives += 1
        elif self.box_type == "ball":
            # Add a brown ball to all balls
            brown_ball = Ball(color=BROWN)
            brown_ball.rect.center = paddle.rect.center
            balls_sprite.add(brown_ball)
            all_sprites.add(brown_ball)

        self.kill()
        return fps,dizziness_mode,lives,BOX_TYPES[self.box_type]
