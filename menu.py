import pygame

class Menu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 72)
        self.instruction_font = pygame.font.Font(None, 28)
        self.button_width = 200
        self.button_height = 50
        self.start_button = pygame.Rect(width // 2 - self.button_width // 2, height // 2 - 75, self.button_width, self.button_height)
        self.how_to_play_button = pygame.Rect(width // 2 - self.button_width // 2, height // 2 - 12.5, self.button_width, self.button_height)
        self.exit_button = pygame.Rect(width // 2 - self.button_width // 2, height // 2 + 50, self.button_width, self.button_height)
        self.back_button = pygame.Rect(20, height - 70, 100, 40)
        self.hovered_button = None
        self.title_text = self.title_font.render("Brick Buster", True, (255, 255, 255))
        self.instructions = [
            "How to Play:",
            "1. Use the left and right arrow keys or mouse to move the paddle.",
            "2. Break all the bricks by hitting them with the ball.",
            "3. Don't let the ball fall below the paddle.",
            "4. Press 'C' to change music after starting the game.",
            "5. Press 'M' to mute the music after starting the game.",
            "6. Catch power-ups to enhance your gameplay.",
            "7. Enjoy the game and aim for a high score!"
        ]
        self.show_instructions = False

    def draw(self):
        self.screen.blit(self.title_text, (self.width // 2 - self.title_text.get_width() // 2, 50))
        if not self.show_instructions:
            # Draw buttons with gradient colors
            self.draw_button(self.start_button, (51, 153, 255), (0, 102, 255), "Start")
            self.draw_button(self.how_to_play_button, (51, 153, 255), (0, 102, 255), "How to Play")
            self.draw_button(self.exit_button, (51, 153, 255), (0, 102, 255), "Exit")

            # Check if mouse is hovering over buttons
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_button = None
            if self.start_button.collidepoint(mouse_pos):
                self.draw_button(self.start_button, (102, 178, 255), (0, 51, 204), "Start", hovered=True)
                self.hovered_button = "start"
            if self.how_to_play_button.collidepoint(mouse_pos):
                self.draw_button(self.how_to_play_button, (102, 178, 255), (0, 51, 204), "How to Play", hovered=True)
                self.hovered_button = "how_to_play"
            if self.exit_button.collidepoint(mouse_pos):
                self.draw_button(self.exit_button, (102, 178, 255), (0, 51, 204), "Exit", hovered=True)
                self.hovered_button = "exit"
        else:
            self.display_instructions()

    def draw_button(self, rect, color_top, color_bottom, text, hovered=False):
        # Draw button with gradient color
        pygame.draw.rect(self.screen, color_top, rect, border_radius=10)
        pygame.draw.rect(self.screen, color_bottom, (rect.left, rect.centery, rect.width, rect.height // 2), border_radius=10)
        if hovered:
            pygame.draw.rect(self.screen, (255, 255, 255), rect, width=3, border_radius=10)
        button_text = self.font.render(text, True, (255, 255, 255))
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)

    def handle_event(self, event):
        if not self.show_instructions:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered_button == "start":
                    return "start"
                elif self.hovered_button == "how_to_play":
                    self.show_instructions = True
                elif self.hovered_button == "exit":
                    return "exit"
        else:
            if self.handle_back_button(event):
                self.show_instructions = False

    def display_instructions(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        y_offset = 100
        for line in self.instructions:
            text_surface = self.instruction_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 50
        self.draw_button(self.back_button, (51, 153, 255), (0, 102, 255), "Back", hovered=self.back_button.collidepoint(pygame.mouse.get_pos()))

    def handle_back_button(self, event):
        self.screen.fill((0, 0, 0))  # Clear the screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.show_instructions = False
                return True
        return False
