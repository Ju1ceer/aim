import pygame
from pythonProject1.defs.utils_go_back import Color, screen

def cul_final_score(score, total_clicks):
    """
    计算最终得分。
    :param score: 当前得分
    :param total_clicks: 总点击次数
    :return: 最终得分
    """
    hit_rate = (score / total_clicks * 100) if total_clicks > 0 else 0  # 计算命中率
    if hit_rate < 90:
        return score * 0.9  # 如果命中率低于 90%，得分打 9 折
    return score  # 否则返回原始得分

def draw_score_and_hit_rate(score, total_clicks, time_limit, game_started):
    """
    绘制得分、命中率和剩余时间。
    """
    if not game_started:
        return  # 如果游戏未开始，不绘制任何内容

    score_font = pygame.font.SysFont('Arial', 24)  # 设置字体
    font_color = Color.white  # 字体颜色
    y_offset = 10  # 竖直方向的偏移量

    # 绘制得分
    score_text = score_font.render(f'Score: {score}', True, font_color)
    screen.blit(score_text, (10, y_offset))
    y_offset += 30  # 下移 30 像素

    # 绘制命中率
    if total_clicks > 0:
        hit_rate = score / total_clicks * 100  # 计算命中率
    else:
        hit_rate = 0.0
    hit_rate_text = score_font.render(f'Hit Rate: {hit_rate:.2f}%', True, font_color)
    screen.blit(hit_rate_text, (10, y_offset))
    y_offset += 30  # 下移 30 像素

    # 绘制剩余时间
    minutes, seconds = divmod(int(time_limit), 60)  # 将秒数转换为分钟和秒
    time_text = score_font.render(f'Time: {minutes:02d}:{seconds:02d}', True, font_color)
    screen.blit(time_text, (10, y_offset))  # 绘制剩余时间

def show_score(final_score):
    """
    显示最终得分。
    """
    font = pygame.font.SysFont('Arial', 24)  # 设置字体
    text = font.render(f'Final Score: {final_score}', True, Color.white)  # 渲染文本
    screen.blit(text, (10, 10))  # 绘制文本