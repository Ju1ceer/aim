import pygame
from pythonProject1.defs.utils_go_back import Color, screen

def draw_target(game_started, target_pos, target_radius):
    """
    绘制目标。
    """
    if game_started and target_pos:
        for pos in target_pos:
            if pos:
                pygame.draw.circle(screen, Color.yellow, pos, target_radius)  # 绘制黄色圆形目标

class Game:
    def __init__(self):
        # 游戏设置
        self.running = True  # 游戏运行状态
        self.cursor_radius = 5  # 鼠标指针圆点的半径
        self.score = 0  # 当前得分
        self.final_score = 0  # 最终得分
        self.total_clicks = 0  # 总点击次数
        self.game_started = False  # 游戏是否开始
        self.time_limit = 60  # 时间限制（60秒）
        self.clock = pygame.time.Clock()  # 游戏时钟