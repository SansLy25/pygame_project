import pygame

class Animation:
    def __init__(self, frames_paths, frame_duration):
        """
        во frames указать пути до всех кадров анимации
        :param frames_paths: list[str]
        """
        self.frames = [pygame.image.load(frames_path) for frames_path in
                       frames_paths]
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.frame_duration:
            self.last_update_time = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame]