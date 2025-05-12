import random
import pygame
import numpy as np
from collections import deque
import math
n, m = 27, 27

directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

def is_valid(x, y):
    return 0 < x < n-1 and 0 < y < m-1

def dfs(x, y, maze = np.ones((n, m), dtype=int), path = []):
    maze[x][y] = 0
    random.shuffle(directions)
    open = [(x, y)]
    while open:
        X, Y = open.pop()
        for dx, dy in directions:
            nx, ny = X + dx, Y + dy
            if is_valid(nx, ny) and maze[nx][ny] == 1:
                wall_x, wall_y = X + dx // 2, Y + dy // 2
                maze[wall_x][wall_y] = 0
                open.append((nx, ny))
                path.append(maze.copy())
                dfs(nx, ny, maze, path)
    return path
def bfs(x, y, maze = np.ones((n, m), dtype=int), path = []):
    maze[x][y] = 0
    random.shuffle(directions)
    open = deque([(x, y)])
    while open:
        X, Y = open.popleft()
        for dx, dy in directions:
            nx, ny = X + dx, Y + dy
            if is_valid(nx, ny) and maze[nx][ny] == 1:
                wall_x, wall_y = X + dx // 2, Y + dy // 2
                maze[wall_x][wall_y] = 0
                open.append((nx, ny))
                path.append(maze.copy())
                bfs(nx, ny, maze, path)
    return path
def prim_maze(n, m, start_x=1, start_y=1):
    if n < 3 or m < 3:
        return [np.zeros((n, m), dtype=int)]

    maze = np.ones((n, m), dtype=int)
    path = []

    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < m

    x = start_x
    y = start_y
    maze[x][y] = 0
    path.append(maze.copy())

    walls = []
    for dx, dy in [(-2,0), (2,0), (0,-2), (0,2)]:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny):
            walls.append((nx, ny, x, y))

    while walls:
        wx, wy, fx, fy = walls.pop(random.randint(0, len(walls)-1))
        nx, ny = wx, wy
        mid_x, mid_y = (fx + nx)//2, (fy + ny)//2

        if is_valid(nx, ny) and maze[nx][ny] == 1:
            maze[mid_x][mid_y] = 0
            maze[nx][ny] = 0
            path.append(maze.copy())

            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2)]:
                nnx, nny = nx + dx, ny + dy
                if is_valid(nnx, nny) and maze[nnx][nny] == 1:
                    walls.append((nnx, nny, nx, ny))
    
    return path

def add_extra_connections(maze, percent=0.1):
    """Đục thêm một số tường ngẫu nhiên để tạo nhiều đường đi"""
    wall_candidates = []
    for i in range(1, n-1):
        for j in range(1, m-1):
            if maze[i][j] == 1:
                # Xem có đường ở hai bên không? Nếu có, có thể đục
                neighbors = 0
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    if maze[i+dx][j+dy] == 0:
                        neighbors += 1
                if neighbors >= 2:  # tường giữa 2 đường
                    wall_candidates.append((i, j))

    # Đục một phần tường đã chọn
    count = int(len(wall_candidates) * percent)
    for (x, y) in random.sample(wall_candidates, count):
        maze[x][y] = 0
def draw_maze(screen, maze):
    for i in range(n):
        for j in range(m):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, 'black', (j * 30, i * 30, 30, 30))
def random_goal(maze):
    x = random.randint(1, n-2)
    y = random.randint(1, m-2)
    if maze[x][y] == 0:
        return x,y
    else:
        return random_goal(maze)
def random_start():
    x = random.randint(1, n-2)
    y = random.randint(1, m-2)
    return x,y