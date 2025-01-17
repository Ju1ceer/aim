import pygame

def draw_mainmenu():
    from defs.utils_go_back import Button, buttonstyle, screen_width, screen_height, screen
    from quick_shot import draw_quick_shot
    from six_shots import draw_six_shots

    # 初始化 pygame 模块
    pygame.init()

    # 创建按钮
    button_six_shots = Button(screen_width // 2 - 75, screen_height // 2 - 150, 150, 50, 'Six Shots',
                              buttonstyle.button_font,
                              buttonstyle.button_color, buttonstyle.text_color)  # 六目标模式按钮
    button_quick_shot = Button(screen_width // 2 - 75, screen_height // 2 - 50, 150, 50, 'Quick Shot',
                               buttonstyle.button_font,
                               buttonstyle.button_color, buttonstyle.text_color)  # 快速射击模式按钮
    button_exit = Button(screen_width // 2 - 75, screen_height // 2 + 50, 150, 50, 'Exit', buttonstyle.button_font,
                         buttonstyle.button_color, buttonstyle.text_color)  # 退出按钮

    # 加载背景图片并居中
    try:
        background_image = pygame.image.load('img/Ayanami_rain.jpg')  # 加载背景图片
        original_width, original_height = background_image.get_size()  # 获取图片原始尺寸
        scale_factor = screen_width / original_width  # 计算缩放比例
        scaled_height = int(original_height * scale_factor)  # 计算缩放后的高度
        background_image = pygame.transform.scale(background_image, (screen_width, scaled_height))  # 缩放图片
        y_offset = (screen_height - scaled_height) // 2  # 计算垂直偏移量
        background_rect = background_image.get_rect(topleft=(0, y_offset))  # 设置图片位置
    except pygame.error as e:
        print(f"无法加载背景图片：{e}")  # 如果加载失败，打印错误信息
        background_image = None  # 设置背景图片为 None

    class Go:
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

        def draw_menu(self, screen, buttons):
            """
            绘制主菜单界面。
            """
            screen.fill((0, 0, 0))  # 填充背景色
            if background_image:
                screen.blit(background_image, background_rect)  # 绘制背景图片
            for button in buttons.values():
                button.draw(screen)  # 绘制所有按钮

    # 创建按钮字典
    buttons = {
        'six_shots': button_six_shots,  # 六目标模式按钮
        'quick_shot': button_quick_shot,  # 快速射击模式按钮
        'exit': button_exit,  # 退出按钮
    }
    game_state = Go()  # 创建游戏状态管理对象

    # 游戏主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # 如果检测到退出事件，停止循环
            game_state.handle_events(event, buttons)  # 处理事件

        game_state.draw(screen, buttons)  # 绘制界面
        pygame.display.flip()  # 更新屏幕显示

    # 退出 pygame
    pygame.quit()

# 调用主菜单函数
draw_mainmenu()