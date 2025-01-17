def draw_quick_shot(screen):
    import pygame
    import random
    global sql_score  # 全局变量，用于存储数据库中的得分
    from defs.game_state import draw_target, Game
    from defs.score_on_window import cul_final_score, show_score, draw_score_and_hit_rate
    from defs.leaderboard import get_quickshot_leaderboard, show_leaderboard
    from defs.sql import get_player_name, insert_score_quickshot
    from defs.utils_go_back import Color, Button, buttonstyle, screen_width, screen_height, screen
    from mainmenu import draw_mainmenu

    # 初始化 pygame
    pygame.init()

    # 游戏设置
    game = Game()  # 创建游戏状态管理对象
    target_pos = [None, None, None, None, None, None, None]  # 目标位置列表
    target_radius = 34  # 目标半径
    sql_score = 0
    # 加载背景图片并居中
    try:
        background_image = pygame.image.load('img/wind.jpg')  # 加载背景图片
        original_width, original_height = background_image.get_size()  # 获取图片原始尺寸
        scale_factor = screen_width / original_width  # 计算缩放比例
        scaled_height = int(original_height * scale_factor)  # 计算缩放后的高度
        background_image = pygame.transform.scale(background_image, (screen_width, scaled_height))  # 缩放图片
        y_offset = (screen_height - scaled_height) // 2  # 计算垂直偏移量
        background_rect = background_image.get_rect(topleft=(0, y_offset))  # 设置图片位置
    except pygame.error as e:
        print(f"无法加载背景图片：{e}")  # 如果加载失败，打印错误信息
        background_image = None  # 设置背景图片为 None

    # 初始化目标位置函数
    number = 5
    lattice_pos = [
        [
            (
                (target_radius * 2 * i + target_radius) + screen_width // 2 - 200,
                (target_radius * 2 * j + target_radius) + screen_height // 2 - 200
            )
            for j in range(number)
        ]
        for i in range(number)
    ]  # 生成网格位置

    def init_target():
        """
        初始化目标位置。
        """
        available_positions = [pos for row in lattice_pos for pos in row if pos not in target_pos]  # 获取可用位置
        if available_positions:
            return random.choice(available_positions)  # 随机选择一个可用位置
        else:
            return random.choice([pos for row in lattice_pos for pos in row])  # 如果无可用位置，随机选择一个位置

    # 创建按钮对象
    button_go = Button(
        screen_width // 2 - 70, screen_height // 2 - 100, 150, 50, 'Start',
        buttonstyle.button_font, buttonstyle.button_color, buttonstyle.text_color
    )  # 开始按钮
    button_back = Button(
        screen_width // 2 - 70, screen_height // 2, 150, 50, 'Back To Menu',
        buttonstyle.button_font, buttonstyle.button_color, buttonstyle.text_color
    )  # 返回主菜单按钮
    button_leaderboard = Button(
        screen_width - 60, 10, 50, 50,  # 放置在右上角
        text=None,  # 不需要文本
        font=None,  # 不需要字体
        color=None,  # 不需要背景颜色
        text_color=None,  # 不需要文本颜色
        image_path='icon/crosshairs-solid.svg'  # 使用图片作为按钮
    )  # 排行榜按钮

    def ski():
        """
        显示最终得分并绘制按钮。
        """
        show_score(game.final_score)  # 显示最终得分
        button_go.draw(screen)  # 绘制开始按钮
        button_back.draw(screen)  # 绘制返回主菜单按钮
        button_leaderboard.draw(screen)  # 绘制排行榜按钮

    # 游戏主循环
    while game.running:
        screen.fill(Color.black)  # 填充背景色
        if background_image:
            screen.blit(background_image, background_rect)  # 绘制背景图片

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False  # 如果检测到退出事件，停止循环
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # 获取鼠标点击位置
                if not game.game_started:
                    if button_go.lil_is_clicked(pos):
                        game.game_started = True  # 开始游戏
                        pygame.mouse.set_visible(False)  # 隐藏鼠标光标
                        target_pos = [init_target() for _ in range(4)]  # 初始化目标位置
                    elif button_back.lil_is_clicked(pos):
                        draw_mainmenu()  # 返回主菜单
                    elif button_leaderboard.lil_is_clicked(pos):
                        leaderboard = get_quickshot_leaderboard()  # 获取排行榜数据
                        show_leaderboard(screen, leaderboard)  # 显示排行榜
                elif game.game_started:
                    game.total_clicks += 1  # 增加总点击次数
                    for i in range(4):  # 遍历前 4 个目标
                        if target_pos[i] and (  # 检查目标是否存在
                                (pos[0] - target_pos[i][0]) ** 2 + (pos[1] - target_pos[i][1]) ** 2 ) <= target_radius ** 2:  # 检查点击位置是否在目标范围内
                            game.score += 1  # 如果命中目标，增加得分
                            target_pos[i] = init_target()  # 重新初始化目标位置
            elif event.type == pygame.KEYDOWN:  # 检测键盘按键事件
                if event.key == pygame.K_ESCAPE:  # 如果按下 ESC 键
                    game.game_started = False  # 停止游戏
                    pygame.mouse.set_visible(True)
                    ski()
                    return
        # 更新时间
        if game.game_started:
            game.time_limit -= game.clock.tick(60) / 1000  # 减少时间限制
            if game.time_limit <= 0:
                game.game_started = False  # 停止游戏
                game.final_score = cul_final_score(game.score, game.total_clicks)  # 计算最终得分
                sql_score = cul_final_score(game.score, game.total_clicks)  # 存储得分到 SQL
                game.score = 0  # 重置得分
                game.total_clicks = 0  # 重置总点击次数
                game.time_limit = 60  # 重置时间限制
                target_pos = [None] * 8  # 重置目标位置

        if game.game_started:
            draw_target(game.game_started, target_pos, target_radius)  # 绘制目标
            draw_score_and_hit_rate(game.score, game.total_clicks, game.time_limit, game.game_started)  # 绘制得分信息
        else:
            ski()  # 调用 ski() 函数

        # 未开始或结束时的处理
        if not game.game_started:
            pygame.mouse.set_visible(True)  # 显示鼠标光标
            if sql_score > 0:
                player_name = get_player_name(screen)  # 获取玩家名字
                if player_name:
                    insert_score_quickshot(player_name, game.final_score)  # 插入得分到数据库
                    pygame.display.flip()  # 更新屏幕显示
                    sql_score = 0  # 重置 SQL 得分
                    ski()  # 调用 ski() 函数
        else:
            pygame.mouse.set_visible(False)  # 隐藏鼠标光标
            pygame.draw.circle(screen, Color.black, pygame.mouse.get_pos(), game.cursor_radius)  # 绘制自定义光标

        pygame.display.flip()  # 更新屏幕显示

    pygame.quit()  # 退出游戏