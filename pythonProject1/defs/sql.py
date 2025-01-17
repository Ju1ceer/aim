import pygame
import pymysql
from pythonProject1.defs.utils_go_back import screen_width, screen_height, Color

def connect_to_database():
    """
    连接数据库。
    :return: 数据库连接对象
    """
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db='game_db'
        )
        return connection
    except Exception as e:
        print(f"连接数据库失败: {e}")  # 如果连接失败，打印错误信息
        return None

def insert_score(table_name, name, score):
    """
    插入或更新得分。
    :param table_name: 表名
    :param name: 玩家名字
    :param score: 玩家得分
    """
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 使用 ON DUPLICATE KEY UPDATE 插入或更新得分
                sql = f"""
                INSERT INTO {table_name} (name, score) 
                VALUES (%s, %s) 
                ON DUPLICATE KEY UPDATE 
                score = IF(VALUES(score) > score, VALUES(score), score);
                """
                cursor.execute(sql, (name, score))  # 执行 SQL 语句
            connection.commit()  # 提交事务
            print(f"插入或更新成功: {name} - {score}（表: {table_name}）")
        except Exception as e:
            print(f"插入或更新数据失败: {e}")  # 如果操作失败，打印错误信息
        finally:
            connection.close()  # 关闭数据库连接

def insert_score_quickshot(name, score):
    """
    插入快速射击得分。
    """
    insert_score('quick_shot_scores', name, score)

def insert_score_sixshots(name, score):
    """
    插入六目标得分。
    """
    insert_score('six_shot_scores', name, score)

def get_player_name(screen):
    """
    获取玩家名字。
    :return: 玩家名字
    """
    import pygame.locals as pl
    font = pygame.font.SysFont('Arial', 24)  # 设置字体
    input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 20, 200, 40)  # 创建输入框
    text = ''  # 初始化输入文本
    while True:
        for event in pygame.event.get():
            if event.type == pl.QUIT:
                return 'quit'  # 如果检测到退出事件，返回 'quit'
            if event.type == pl.KEYDOWN:
                if event.key == pl.K_RETURN:
                    print(f"输入的名字是: {text}")  # 如果按下回车键，返回输入的名字
                    return text
                elif event.key == pl.K_ESCAPE:
                    return ''  # 如果按下 ESC 键，返回空字符串
                elif event.key == pl.K_BACKSPACE:
                    text = text[:-1]  # 如果按下退格键，删除最后一个字符
                else:
                    text += event.unicode  # 添加输入的字符
        screen.fill(Color.black)  # 填充背景色
        # 加载背景图片并居中
        try:
            background_image = pygame.image.load('img/1.jpg')
            original_width, original_height = background_image.get_size()
            scale_factor = screen_width / original_width
            scaled_height = int(original_height * scale_factor)
            background_image = pygame.transform.scale(background_image, (screen_width, scaled_height))
            y_offset = (screen_height - scaled_height) // 2
            background_rect = background_image.get_rect(topleft=(0, y_offset))
        except pygame.error as e:
            print(f"无法加载背景图片：{e}")
            background_image = None

        if background_image:
            screen.blit(background_image, background_rect)  # 绘制背景图片
        txt_surface = font.render(text, True, Color.black)  # 渲染输入文本
        input_text = font.render("Enter your id (please keep it unique)", True, Color.black)  # 渲染提示文本
        screen.blit(input_text, (screen_width // 2 - 100, screen_height // 2 - 50))  # 绘制提示文本
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))  # 绘制输入文本
        pygame.draw.rect(screen, Color.black, input_box, 2)  # 绘制输入框边框
        pygame.display.flip()  # 更新屏幕显示