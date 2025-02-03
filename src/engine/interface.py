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


class ExperienceBar:
    def __init__(self, x, y, width, height, max_exp, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_exp = max_exp
        self.current_exp = 0
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 2)
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
        fill_width = int((self.current_exp / self.max_exp) * self.width)
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, fill_width, self.height))
        font = pygame.font.Font(None, 25)
        exp_text = f"{self.current_exp}/{self.max_exp}"
        text_surface = font.render(exp_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        self.screen.blit(text_surface, text_rect)

    def set_exp(self, current_exp):
        self.current_exp = current_exp

    def add_exp(self, add_value):
        self.current_exp += add_value

    def set_max(self, max_exp):
        self.max_exp = max_exp


class UpgradeManager:
    def __init__(self, screen):
        self.screen = screen
        self.hp_sprite = pygame.transform.scale(pygame.image.load('../assets/max_hp_icon.png'),
                                                        (130, 90))
        self.damage_sprite = pygame.transform.scale(pygame.image.load('../assets/attack_icon.png'),
                                                (130, 90))
        self.attack_speed_sprite = pygame.transform.scale(pygame.image.load('../assets/attack_speed_icon.png'),
                                                (130, 90))
        self.crit_sprite = pygame.transform.scale(pygame.image.load('../assets/crit_icon.png'),
                                                (130, 90))
        self.crit_chance_sprite = pygame.transform.scale(pygame.image.load('../assets/crit_chance_icon.png'),
                                                (130, 90))
        self.hp_button = Button(150, 80, 625, 90, 'Повышает максимальное здоровье на 100', '../assets/Default.png', self.screen)
        self.damage_button = Button(150, 170, 625, 90, 'Повышает урон от атаки на 20%', '../assets/Default.png', self.screen)
        self.attack_speed_button = Button(150, 260, 625, 90, 'Повышает скорость атаки на 0.5 единиц', '../assets/Default.png', self.screen)
        self.crit_button = Button(150, 350, 625, 90, 'Повышает критический урон на 20%', '../assets/Default.png', self.screen)
        self.crit_chance_button = Button(150, 440, 625, 90, 'Повышает шанс критического удара на 2%', '../assets/Default.png', self.screen)
        self.cancel_button = Button(150, 540, 625, 50, 'Закрыть',
                                        '../assets/Default.png', self.screen)

    def draw(self):
        self.hp_button.draw()
        self.attack_speed_button.draw()
        self.damage_button.draw()
        self.crit_button.draw()
        self.crit_chance_button.draw()
        self.cancel_button.draw()
        self.screen.blit(self.hp_sprite, (10, 80))
        self.screen.blit(self.damage_sprite, (10, 170))
        self.screen.blit(self.attack_speed_sprite, (10, 260))
        self.screen.blit(self.crit_sprite, (10, 350))
        self.screen.blit(self.crit_chance_sprite, (10, 440))
