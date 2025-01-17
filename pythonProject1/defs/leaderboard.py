import pygame
from pythonProject1.defs.sql import connect_to_database
from pythonProject1.defs.utils_go_back import screen_width, Color

def get_leaderboard(table_name):
    """
    获取指定表的得分榜。
    :param table_name: 表名
    :return: 得分榜数据（列表形式）
    """
    connection = connect_to_database()
    leaderboard = []
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = f"SELECT name, score FROM {table_name} ORDER BY score DESC LIMIT 10"  # 查询前 10 名
                cursor.execute(sql)
                result = cursor.fetchall()  # 获取查询结果
                leaderboard = result
        except Exception as e:
            print(f"读取数据失败: {e}")  # 如果查询失败，打印错误信息
        finally:
            connection.close()  # 关闭数据库连接
    return leaderboard

def get_sixshot_leaderboard():
    """
    获取六目标模式的得分榜。
    """
    return get_leaderboard('six_shot_scores')

def get_quickshot_leaderboard():
    """
    获取快速射击模式的得分榜。
    """
    return get_leaderboard('quick_shot_scores')

def show_leaderboard(screen, leaderboard):
    """
    显示得分榜。
    """
    import pygame.locals as pl
    font = pygame.font.SysFont('Arial', 24)  # 设置字体
    title_font = pygame.font.SysFont('Arial', 36)  # 设置标题字体
    y_offset = 170  # 竖直方向的偏移量

    # 加载按钮图片
    try:
        button_image = pygame.image.load('icon/crosshairs-solid.svg')  # 加载图片
        button_image = pygame.transform.scale(button_image, (50, 50))  # 调整图片大小
        button_rect = button_image.get_rect(topright=(screen_width - 10, 10))  # 放置到右上角
    except pygame.error as e:
        print(f"无法加载按钮图片: {e}")  # 如果加载失败，打印错误信息
        button_image = None
        button_rect = pygame.Rect(screen_width - 60, 10, 50, 50)  # 使用默认矩形按钮

    # 绘制标题
    title_text = title_font.render("LeaderBoard", True, Color.white)  # 渲染标题文本
    screen.blit(title_text, (screen_width // 2 - 100, y_offset))  # 绘制标题
    y_offset += 40  # 下移 40 像素

    # 绘制按钮
    if button_image:
        screen.blit(button_image, button_rect)  # 绘制按钮图片

    # 绘制积分榜
    for idx, (name, score) in enumerate(leaderboard, start=1):
        text = font.render(f"{idx}. {name}: {score}", True, Color.white)  # 渲染得分文本
        screen.blit(text, (screen_width // 2 - 100, y_offset))  # 绘制得分文本
        y_offset += 30  # 下移 30 像素

    pygame.display.flip()  # 更新屏幕显示

    # 等待用户点击按钮或按下 ESC 键
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pl.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(pos):  # 检查是否点击了按钮
                    waiting = False  # 停止等待
            elif event.type == pl.KEYDOWN:
                if event.key == pl.K_ESCAPE:
                    waiting = False  # 停止等待