import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.paddle_sound = pygame.mixer.Sound("src/resources/pong_paddle.mp3")
        self.wall_sound = pygame.mixer.Sound("src/resources/pong_wall.mp3")
        self.pong_score_sound = pygame.mixer.Sound("src/resources/pong_score.mp3")
        self.boosted_sound = pygame.mixer.Sound("src/resources/pong_boosted.mp3")
        self.pong_bgm_sound = pygame.mixer.music.load("src/resources/pong_bgm.mp3")

        self.button_sound = pygame.mixer.Sound("src/resources/button.mp3")

        self.jump_sound = pygame.mixer.Sound("src/resources/longjump_jump.mp3")
        self.longjump_score_sound = pygame.mixer.Sound(
            "src/resources/longjump_score.mp3"
        )
        self.longjump_bgm_sound = pygame.mixer.music.load(
            "src/resources/longjump_bgm.mp3"
        )

    def play_paddle_sound(self):
        self.paddle_sound.play()

    def play_wall_sound(self):
        self.wall_sound.play()

    def play_pong_score_sound(self):
        self.pong_score_sound.play()

    def play_boosted_sound(self):
        self.boosted_sound.play()

    def play_pong_bgm_sound(self):
        self.pong_bgm_sound = pygame.mixer.music.load("src/resources/pong_bgm.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

    def play_button_sound(self):
        self.button_sound.play()

    def play_jump_sound(self):
        self.jump_sound.play()

    def play_longjump_score_sound(self):
        self.longjump_score_sound.play()

    def play_longjump_bgm_sound(self):
        self.longjump_bgm_sound = pygame.mixer.music.load(
            "src/resources/longjump_bgm.mp3"
        )
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
