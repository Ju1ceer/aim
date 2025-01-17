import pygame
from quick_shot import draw_quick_shot
from six_shots import draw_six_shots

# 初始化 pygame
pygame.init()

# 设置窗口大小
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))

class Color:
    white = (255, 255, 255)
    red = (255, 0, 0)
    black = (0, 0, 0)
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    diy = (174, 24, 74)

class buttonstyle:
    button_font = pygame.font.SysFont('Arial', 22, True)  # 按钮字体
    button_color = Color.diy  # 按钮背景颜色
    text_color = Color.white  # 按钮文本颜色

class Button:
    def __init__(self, x, y, width, height, text=None, font=None, color=None, text_color=None, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)  # 按钮的矩形区域
        self.text = text  # 按钮文本
        self.font = font  # 按钮字体
        self.color = color  # 按钮背景颜色
        self.text_color = text_color  # 按钮文本颜色
        self.image = None  # 按钮图片
        if image_path:
            try:
                self.image = pygame.image.load(image_path)  # 加载按钮图片
                self.image = pygame.transform.scale(self.image, (width, height))  # 调整图片大小
            except pygame.error as e:
                print(f"无法加载按钮图片: {e}")  # 如果加载失败，打印错误信息

    def draw(self, screen):
        """
        绘制按钮。
        """
        if self.image:
            screen.blit(self.image, self.rect.topleft)  # 绘制图片
        else:
            pygame.draw.rect(screen, self.color, self.rect)  # 绘制矩形背景
            if self.text:
                text_surface = self.font.render(self.text, True, self.text_color)  # 渲染文本
                text_rect = text_surface.get_rect(center=self.rect.center)  # 设置文本位置
                screen.blit(text_surface, text_rect)  # 绘制文本

    def is_clicked(self, event, pos):
        """
        检测按钮是否被点击。
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
            return True
        return False

    def lil_is_clicked(self, pos):
        """
        检测按钮是否被点击（简化版）。
        """
        return self.rect.collidepoint(pos)

class Back:
    def __init__(self):
        self.state = 'menu'  # 默认状态为菜单

    def handle_events(self, event, buttons):
        """
        处理事件，根据点击的按钮切换游戏状态。
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()  # 获取鼠标点击位置
            if self.state == 'menu':
                if buttons['six_shots'].is_clicked(event, pos):
                    self.state = 'six_shots'  # 切换到六目标模式
                elif buttons['quick_shot'].is_clicked(event, pos):
                    self.state = 'quick_shot'  # 切换到快速射击模式
                elif buttons['exit'].is_clicked(event, pos):
                    self.state = 'exit'  # 退出游戏

    def draw(self, screen, buttons):
        """
        根据当前状态绘制界面。
        """
        if self.state == 'menu':
            self.draw_menu(screen, buttons)  # 绘制主菜单
        elif self.state == 'six_shots':
            draw_six_shots(screen)  # 进入六目标模式
        elif self.state == 'quick_shot':
            draw_quick_shot(screen)  # 进入快速射击模式
        elif self.state == 'exit':
            pygame.quit()  # 退出 pygame
            quit()  # 退出程序