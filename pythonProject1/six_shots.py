def draw_six_shots(screen):
    # 导入必要的模块
    import pygame
    import random
    global sql_score  # 全局变量，用于存储数据库中的得分

    # 从自定义模块中导入必要的函数和类
    from pythonProject1.defs.game_state import draw_target, Game
    from pythonProject1.defs.score_on_window import cul_final_score, show_score, draw_score_and_hit_rate
    from pythonProject1.defs.leaderboard import show_leaderboard, get_sixshot_leaderboard
    from pythonProject1.defs.sql import get_player_name, insert_score_sixshots
    from pythonProject1.mainmenu import draw_mainmenu
    from pythonProject1.defs.utils_go_back import Color, Button, buttonstyle, screen_width, screen_height, screen

    # 初始化 pygame 模块
    pygame.init()

    # 设置游戏参数
    target_pos = [None] * 6  # 存储6个目标的位置，初始为 None
    target_radius = 14  # 目标的半径
    game = Game()  # 创建游戏状态管理对象，用于跟踪得分、时间、点击次数等
    sql_score = 0
    # 加载并缩放背景图片
    try:
        # 加载背景图片
        background_image = pygame.image.load('img/water.jpg')
        # 获取图片的原始尺寸
        original_width, original_height = background_image.get_size()
        # 计算缩放比例，使图片宽度适应屏幕宽度
        scale_factor = screen_width / original_width
        # 计算缩放后的高度
        scaled_height = int(original_height * scale_factor)
        # 缩放图片
        background_image = pygame.transform.scale(background_image, (screen_width, scaled_height))
        # 计算图片的垂直偏移量，使其居中
        y_offset = (screen_height - scaled_height) // 2
        # 设置图片的位置
        background_rect = background_image.get_rect(topleft=(0, y_offset))
    except pygame.error as e:
        # 如果图片加载失败，打印错误信息并设置背景图片为 None
        print(f"无法加载背景图片：{e}")
        background_image = None

    # 定义初始化目标位置的函数
    def init_target():
        """
        随机生成一个目标的位置，确保目标在屏幕范围内。
        """
        return (
            random.randint(target_radius, screen_width - target_radius),  # 随机 x 坐标
            random.randint(target_radius, screen_height - target_radius)  # 随机 y 坐标
        )

    # 创建按钮对象
    button_go = Button(
        screen_width // 2 - 70, screen_height // 2 - 100, 150, 50, 'Start',
        buttonstyle.button_font, buttonstyle.button_color, buttonstyle.text_color
    )  # 开始游戏按钮
    button_back = Button(
        screen_width // 2 - 70, screen_height // 2, 150, 50, 'Back To Menu',
        buttonstyle.button_font, buttonstyle.button_color, buttonstyle.text_color
    )  # 返回主菜单按钮
    button_leaderboard = Button(
        screen_width - 60, 10, 50, 50,
        text=None,  # 不需要文本
        font=None,  # 不需要字体
        color=None,  # 不需要背景颜色
        text_color=None,  # 不需要文本颜色
        image_path='icon/crosshairs-solid.svg'  # 使用图片作为按钮
    )  # 显示排行榜按钮

    # 内部函数，用于显示最终得分和按钮
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
        # 填充屏幕背景色
        screen.fill(Color.black)
        # 如果背景图片加载成功，绘制背景图片
        if background_image:
            screen.blit(background_image, background_rect)

        # 处理事件循环
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 如果检测到退出事件，设置游戏运行状态为 False
                game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 如果检测到鼠标点击事件
                pos = pygame.mouse.get_pos()  # 获取鼠标点击的位置
                if not game.game_started:
                    # 如果游戏未开始
                    if button_go.lil_is_clicked(pos):
                        # 如果点击了开始按钮
                        game.game_started = True  # 设置游戏开始状态为 True
                        pygame.mouse.set_visible(False)  # 隐藏鼠标光标
                        target_pos = [init_target() for _ in range(6)]  # 初始化6个目标的位置
                    elif button_back.lil_is_clicked(pos):
                        # 如果点击了返回主菜单按钮
                        draw_mainmenu()  # 调用主菜单绘制函数
                    elif button_leaderboard.lil_is_clicked(pos):
                        # 如果点击了排行榜按钮
                        leaderboard = get_sixshot_leaderboard()  # 获取排行榜数据
                        show_leaderboard(screen, leaderboard)  # 显示排行榜
                elif game.game_started:
                    # 如果游戏已开始
                    game.total_clicks += 1  # 增加总点击次数
                    for i in range(6):
                        # 检查是否命中目标
                        if target_pos[i] and (  # 检查目标是否存在
                                (pos[0] - target_pos[i][0]) ** 2 + (pos[1] - target_pos[i][1]) ** 2 ) <= target_radius ** 2:  # 检查点击位置是否在目标范围内
                            game.score += 1  # 如果命中，增加得分
                            target_pos[i] = init_target()  # 重新初始化该目标的位置
            elif event.type == pygame.KEYDOWN:  # 检测键盘按键事件
                if event.key == pygame.K_ESCAPE:  # 如果按下 ESC 键
                    game.game_started = False  # 停止游戏
                    pygame.mouse.set_visible(True)
                    ski()
                    return
        # 更新时间
        if game.game_started:
            # 如果游戏已开始，减少时间限制
            game.time_limit -= game.clock.tick(60) / 1000
            if game.time_limit <= 0:
                # 如果时间用完
                game.game_started = False  # 设置游戏开始状态为 False
                game.final_score = cul_final_score(game.score, game.total_clicks)  # 计算最终得分
                sql_score = cul_final_score(game.score, game.total_clicks)  # 存储得分到 SQL
                game.score = 0  # 重置得分
                game.time_limit = 60  # 重置时间限制
                game.total_clicks = 0  # 重置总点击次数
                target_pos = [None] * 6  # 重置目标位置



        # 根据游戏状态绘制内容
        if game.game_started:
            # 如果游戏已开始，绘制目标和得分信息
            draw_target(game.game_started, target_pos, target_radius)
            draw_score_and_hit_rate(game.score, game.total_clicks, game.time_limit, game.game_started)
        else:
            # 如果游戏未开始或已结束，调用 ski() 函数
            ski()

        # 未开始或结束时的处理
        if not game.game_started:
            # 如果游戏未开始或已结束
            pygame.mouse.set_visible(True)  # 显示鼠标光标
            if sql_score > 0:
                # 如果有得分
                player_name = get_player_name(screen)  # 获取玩家名字
                if player_name:
                    insert_score_sixshots(player_name, game.final_score)  # 将得分插入数据库
                    pygame.display.flip()  # 更新屏幕显示
                    sql_score = 0  # 重置 SQL 得分
                    ski()  # 调用 ski() 函数
        else:
            # 如果游戏已开始
            pygame.mouse.set_visible(False)  # 隐藏鼠标光标
            pygame.draw.circle(screen, Color.black, pygame.mouse.get_pos(), game.cursor_radius)  # 绘制自定义光标

        # 更新屏幕显示
        pygame.display.flip()

    # 退出 pygame
    pygame.quit()