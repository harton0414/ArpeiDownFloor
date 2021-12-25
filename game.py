# PyGame Engine Startup
import pygame
import os
from core import Core


class Game:
    class Settings:
        WIDTH = 500
        HEIGHT = 600        
        FPS = 60
        TITLE = "阿沛下樓梯"
        FLOOR_SPEEDY = -5
        PLAYER_WIDTH = 50
        PLAYER_HEIGHT = 60

    class Colors:
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

    class GraphicResource:
        def __init__(self):
            # 圖片相關
            self.arpei_img = pygame.transform.scale(pygame.image.load(
                os.path.join("img", "arpei.png")).convert(), (Game.Settings.PLAYER_WIDTH, Game.Settings.PLAYER_HEIGHT))

            self.floor_imgs = []
            for i in range(2):
                self.floor_imgs.append(pygame.image.load(
                    os.path.join("img", f"floor{i}.png")).convert())

    def __init_screen(self):
        # 視窗相關
        self.screen = pygame.display.set_mode(
            (self.Settings.WIDTH, self.Settings.HEIGHT))  # 創建視窗
        pygame.display.set_caption(self.Settings.TITLE)  # 設定標題
        self.clock = pygame.time.Clock()

    def __init_graphics(self):
        self.grapics = self.GraphicResource()

    def __init_sounds(self):
        # 音效相關
        pygame.mixer.init()  # 處理聲音的
        pygame.mixer.music.load(os.path.join("sound", "flogs_loop.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # 播放音效，-1表示無限次播放

    def __init__(self):
        # 初始化
        pygame.init()
        self.__init_screen()
        self.__init_graphics()
        self.__init_sounds()

        self.core = Core(self.Settings,self.grapics)
        # floor_i = 0
        # floor_interval = math.floor(arpei.rect.height * 1.5) / abs(FLOOR_SPEEDY)

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.Settings.FPS)  # 每一秒最多執行幾次

            # 取得input
            for event in pygame.event.get():  # 取得所有事件
                if event.type == pygame.QUIT:
                    self.running = False

            # 更新遊戲
            self.core.update()

            # show
            self.screen.fill(self.Colors.WHITE)
            self.core.all_sprites.draw(self.screen)  # 將sprites畫在screen上
            pygame.display.update()  # 更新display
        pygame.quit()
