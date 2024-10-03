import random
import numpy as np

# 定义瓦片类型
TILES = ["空地", "水域", "草地"]

# 定义相邻约束关系，表示相邻瓦片允许的组合
CONSTRAINTS = {
    "空地": ["空地", "草地"],
    "水域": ["水域", "草地"],
    "草地": ["空地", "水域", "草地"],
}

# 定义地图大小
WIDTH = 5
HEIGHT = 5

# 初始化波函数，每个格子都有可能是所有瓦片
wave_function = [[TILES[:] for _ in range(WIDTH)] for _ in range(HEIGHT)]


# 选择最小熵的格子进行坍缩
def find_min_entropy():
    min_entropy = float('inf')
    min_pos = None

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if len(wave_function[y][x]) > 1:  # 如果格子尚未坍缩
                if len(wave_function[y][x]) < min_entropy:
                    min_entropy = len(wave_function[y][x])
                    min_pos = (x, y)

    return min_pos


# 更新相邻的格子，传播约束
def propagate(x, y):
    stack = [(x, y)]

    while stack:
        cx, cy = stack.pop()
        options = wave_function[cy][cx]

        # 检查上下左右的相邻格子
        neighbors = [
            (cx, cy - 1),  # 上
            (cx, cy + 1),  # 下
            (cx - 1, cy),  # 左
            (cx + 1, cy),  # 右
        ]

        for nx, ny in neighbors:
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                neighbor_options = wave_function[ny][nx]
                new_options = [
                    opt for opt in neighbor_options if any(
                        opt in CONSTRAINTS[o] for o in options
                    )
                ]

                # 如果邻居的可选项有变化，则加入栈中继续传播
                if len(new_options) < len(neighbor_options):
                    wave_function[ny][nx] = new_options
                    stack.append((nx, ny))


# 运行波函数坍缩算法
def collapse():
    while True:
        pos = find_min_entropy()
        if pos is None:
            break  # 所有格子都已坍缩

        x, y = pos
        # 随机选择一个状态进行坍缩
        wave_function[y][x] = [random.choice(wave_function[y][x])]

        # 传播约束
        propagate(x, y)


# 打印生成的地图
def print_map():
    for row in wave_function:
        print(" ".join([tile[0] for tile in row]))


# 主程序
if __name__ == "__main__":
    collapse()
    print_map()
