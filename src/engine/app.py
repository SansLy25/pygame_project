import pygame

from .commons import WIDTH
from .interface import (
    Button,
    Slider,
    Text,
    UpgradeManager,
    ExperienceBar,
    HealthBar,
    BossBar,
)


class App:
    def __init__(self, screen):
        self.screen = screen
        self.is_menu_music = True
        self.upgrade_manager = UpgradeManager(self.screen)
        self.is_lvlup = False
        self.boss_bar = BossBar(WIDTH // 2 - 500, 740, 1000, 50, 500, self.screen)
        self.expbar = ExperienceBar(450, 10, 500, 25, 100, self.screen)
        self.hpbar = HealthBar(60, 700, 50, 100, self.screen)
        self.music_volume = 100
        self.sfx_volume = 100
        self.menu_sprites = pygame.sprite.Group()
        self.play_button = Button(
            50, 275, 160, 85, "Play", "../assets/Default.png", screen
        )
        self.background_sprite = pygame.transform.scale(
            pygame.image.load("../assets/menu_background.jpg"), (1400, 800)
        )
        self.resume_button = Button(
            300, 140, 200, 80, "Resume", "../assets/Default.png", screen
        )
        self.settings_button = Button(
            300, 260, 200, 80, "Settings", "../assets/Default.png", screen
        )
        self.exit_button = Button(
            300, 380, 200, 80, "Exit", "../assets/Default.png", screen
        )
        self.logo_sprite = pygame.transform.scale(
            pygame.image.load("../assets/Logo.png"), (1835 // 3, 751 // 3)
        )
        self.vol1_slider = Slider(
            100, 210, 350, 20, 0, 100, 1, screen, start_value=self.music_volume
        )
        self.vol2_slider = Slider(
            100, 310, 350, 20, 0, 100, 1, screen, start_value=self.sfx_volume
        )
        self.back1_button = Button(
            300, 450, 200, 80, "Back", "../assets/Default.png", screen
        )
        self.settings_text1 = Text(
            "Music volume", 36, 520, 170, 100, 100, (255, 255, 255), screen
        )
        self.game_other = Text(
            "GAME OTHER, YOU DEAD", 100, 660, 250, 100, 100, (255, 0, 0), screen
        )
        self.win = Text(
            "CONGRATULATIONS, YOU WIN!", 100, 660, 250, 100, 100, (0, 255, 0), screen
        )

        self.settings_text2 = Text(
            "SFX volume", 36, 510, 270, 100, 100, (255, 255, 255), screen
        )
        self.pick_button = Button(
            WIDTH // 2 - 170, 690, 160, 100, "Yes", "../assets/Default.png", screen
        )
        self.cancel_button = Button(
            WIDTH // 2 + 10, 690, 160, 100, "No", "../assets/Default.png", screen
        )
        self.text1 = Text(
            "Take this item?",
            36,
            WIDTH // 2 - 50,
            600,
            100,
            100,
            (255, 255, 255),
            screen,
        )

    def start_screen(self):
        if not self.is_menu_music:
            pygame.mixer.music.load("../assets/menuLoop.mp3")
            pygame.mixer.music.play(-1)
            self.is_menu_music = True
        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.logo_sprite, (0, 0))
        self.play_button.draw()

    def death(self, level, rooms_completed, rooms_count):
        self.level = Text(
            f"Your level: {level}", 36, 670, 350, 100, 100, (255, 255, 255), self.screen
        )
        self.rooms_completed = Text(
            f"Rooms completed: {rooms_completed}/{rooms_count}",
            36,
            670,
            400,
            100,
            100,
            (255, 255, 255),
            self.screen,
        )
        self.level.draw()
        self.rooms_completed.draw()
        self.game_other.draw()

    def you_win(self, level, rooms_completed, rooms_count):
        self.level = Text(
            f"Your level: {level}", 36, 670, 350, 100, 100, (255, 255, 255), self.screen
        )
        self.rooms_completed = Text(
            f"Rooms completed: {rooms_completed}/{rooms_count}",
            36,
            670,
            400,
            100,
            100,
            (255, 255, 255),
            self.screen,
        )
        self.rooms_completed.draw()
        self.level.draw()
        self.win.draw()

    def pause(self):
        self.resume_button.draw()
        self.settings_button.draw()
        self.exit_button.draw()

    def settings(self, events):
        self.vol1_slider.update(events)
        self.settings_text1.draw()
        self.settings_text2.draw()
        self.vol2_slider.update(events)
        self.vol1_slider.draw()
        self.vol2_slider.draw()
        self.back1_button.draw()
        self.music_volume = self.vol1_slider.get_value()
        pygame.mixer.music.set_volume(self.music_volume / 100)
        self.sfx_volume = self.vol2_slider.get_value()

    def item_found(self):
        self.pick_button.draw()
        self.cancel_button.draw()
        self.text1.draw()
