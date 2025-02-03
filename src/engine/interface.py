import math
import pygame
from pygame import Rect


class Text:
    def __init__(self, text, size, x, y, width, height, color, screen, font=None):
        self.text = text
        self.screen = screen

        self.size = size

        self.x = x
        self.y = y

        self.color = color

        self.widht = width
        self.height = height

        self.rect = Rect(self.x, self.y, self.widht, self.height)
        self.font = pygame.font.Font(None, self.size)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self):
        self.screen.blit(self.text_surface, self.text_rect)


class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, step, screen, start_value=None):
        self.screen = screen
        self.rect = pygame.Rect(x, y + height // 4, width, height // 2)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = start_value if start_value is not None else min_value
        self.handle_radius = height // 2
        self.handle_pos = x + (self.value - min_value) / (max_value - min_value) * width
        self.dragging = False

    def draw(self):
        pygame.draw.rect(self.screen, (200, 200, 200), self.rect)
        pygame.draw.circle(self.screen, (0, 255, 0), (int(self.handle_pos), self.rect.centery), self.handle_radius)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                distance = math.sqrt((mouse_x - self.handle_pos) ** 2 + (mouse_y - self.rect.centery) ** 2)
                if distance <= self.handle_radius:
                    self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.handle_pos = max(self.rect.left, min(event.pos[0], self.rect.right))
                self.value = self.min_value + (self.handle_pos - self.rect.left) / self.rect.width * (
                        self.max_value - self.min_value)
                self.value = round(self.value / self.step) * self.step
                self.handle_pos = self.rect.left + (self.value - self.min_value) / (
                        self.max_value - self.min_value) * self.rect.width

    def get_value(self):
        return self.value


class Button:
    def __init__(self, x, y, width, height, text, image_path, screen):
        self.x = x
        self.y = y

        self.screen = screen
        self.width = width
        self.height = height

        self.text = text

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_hovered = False

    def draw(self):
        current_image = self.image
        self.screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)