import pygame
from collections import deque
import copy
import random
from queue import PriorityQueue
def Manhattan_Heuristic(current, goal):
    distance = 0
    goal_x, goal_y = goal
    current_x, current_y = current
    distance = abs(current_x - goal_x) + abs(current_y - goal_y)
    return distance
class Algorithm:
    def __init__(self, screen, width_maze, height_maze, cell_size):
        self.screen = screen
        self.width_maze = width_maze
        self.height_maze = height_maze
        self.cell_size = cell_size
        self.Moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def Check(self, x, y):
        return 0 < x < self.height_maze and 0 < y < self.width_maze  # chú ý: height là hàng, width là cột

    def Chinh_Sua_Ma_Tran(self, board, x, y, new_x, new_y):
        new_board = copy.deepcopy(board)
        new_board[new_x][new_y] = 3  # đánh dấu bước đi
        return new_board

    def BFS(self, Maze, start, goal):
        visited = set()
        queue = deque()
        initial_maze = copy.deepcopy(Maze)
        initial_maze[start[0]][start[1]] = 3

        queue.append((start, [initial_maze], [start]))

        while queue:
            (x, y), path, way = queue.popleft()
            if (x, y) == goal:
                return path

            for dx, dy in self.Moves:
                nx, ny = x + dx, y + dy
                if self.Check(nx, ny) and Maze[nx][ny] == 0 and (nx, ny) not in way:
                    new_maze = self.Chinh_Sua_Ma_Tran(path[-1], x, y, nx, ny)
                    queue.append(((nx, ny), path + [new_maze], way + [(nx, ny)]))

        return None
    def DFS(self, Maze, start, goal):
        visited = set()
        open = []
        initial_maze = copy.deepcopy(Maze)
        initial_maze[start[0]][start[1]] = 3
        open.append((start, [initial_maze],[start]))
        while open:
            (x,y), path, way = open.pop()
            if (x,y) == goal:
                return path
            for dx, dy in self.Moves:
                new_x, new_y = x + dx, y + dy
                if self.Check(new_x, new_y) and Maze[new_x][new_y] == 0 and (new_x, new_y) not in way:
                    new_maze = self.Chinh_Sua_Ma_Tran(path[-1], x, y, new_x, new_y)
                    open.append(((new_x,new_y), path + [new_maze], way + [(new_x, new_y)]))
        return None

    def A_Star_Search(self, Maze, start, goal):
        start = tuple(start)
        goal = tuple(goal)
        open = PriorityQueue()

        initial_maze = copy.deepcopy(Maze)
        initial_maze[start[0]][start[1]] = 3

        g_cost = {start: 0}
        f_cost = {start: Manhattan_Heuristic(start, goal)}

        open.put((f_cost[start], g_cost[start], start, [initial_maze], [start]))

        while not open.empty():
            _, g, current, path, way = open.get()
            x, y = current

            if current == goal:
                return path

            for dx, dy in self.Moves:
                new_x, new_y = x + dx, y + dy
                new_pos = (new_x, new_y)

                if self.Check(new_x, new_y) and Maze[new_x][new_y] == 0 and new_pos not in way:
                    new_maze = self.Chinh_Sua_Ma_Tran(path[-1], x, y, new_x, new_y)
                    new_g = g + 1
                    f = new_g + Manhattan_Heuristic(new_pos, goal)
                    if new_pos not in g_cost or new_g < g_cost[new_pos]:
                        g_cost[new_pos] = new_g
                        f_cost[new_pos] = f
                        open.put((f, new_g, new_pos, path + [new_maze], way + [new_pos]))

        return None

    def Steepest_Ascent_Hill_Climbing(self, Maze, start, goal):
        start = tuple(start)
        goal = tuple(goal)
        current = start
        path = []

        # Khởi tạo maze ban đầu với bước đầu tiên được đánh dấu
        maze = copy.deepcopy(Maze)
        maze[current[0]][current[1]] = 3
        path.append(copy.deepcopy(maze))

        while True:
            x, y = current
            neighbors = []

            for dx, dy in self.Moves:
                new_x, new_y = x + dx, y + dy
                if self.Check(new_x, new_y) and Maze[new_x][new_y] == 0:
                    neighbors.append((new_x, new_y))

            if not neighbors:
                break

            # Chọn neighbor có heuristic thấp nhất
            next_state = min(neighbors, key=lambda pos: Manhattan_Heuristic(pos, goal))

            if Manhattan_Heuristic(next_state, goal) >= Manhattan_Heuristic(current, goal):
                break

            # Cập nhật maze và current
            new_x, new_y = next_state
            maze = self.Chinh_Sua_Ma_Tran(maze, x, y, new_x, new_y)
            path.append(copy.deepcopy(maze))
            current = next_state

        return path
    def Beam_Search(self, Maze, Start, Goal, beam_width=3):
        Start = tuple(Start)
        Goal = tuple(Goal)
        current_level = [(Start, [copy.deepcopy(Maze)])]
        visited = set()
        visited.add(Start)

        while current_level:
            next_level_candidates = PriorityQueue()

            for state, path in current_level:
                if state == Goal:
                    return path

                x, y = state
                for dx, dy in self.Moves:
                    nx, ny = x + dx, y + dy
                    new_pos = (nx, ny)
                    if self.Check(nx, ny) and Maze[nx][ny] == 0 and new_pos not in visited:
                        visited.add(new_pos)
                        new_maze = self.Chinh_Sua_Ma_Tran(path[-1], x, y, nx, ny)
                        heuristic = Manhattan_Heuristic(new_pos, Goal)
                        next_level_candidates.put((heuristic, new_pos, path + [new_maze]))

            current_level = []
            for _ in range(min(beam_width, next_level_candidates.qsize())):
                _, new_state, new_path = next_level_candidates.get()
                current_level.append((new_state, new_path))

        return None

    def q_study(self, Maze, start, goal, epsilon=0.01, episodes=1000000):
        start = tuple(start)
        goal = tuple(goal)
        q_table = {}
        
        for i in range(self.height_maze):
            for j in range(self.width_maze):
                if Maze[i][j] == 0:
                    q_table[(i, j)] = [0, 0, 0, 0]  # 4 hướng: trên, dưới, trái, phải

        path_mazes = []
        way = []
        
        for episode in range(episodes):
            current_state = start
            way = [current_state]
            path_mazes = []

            # bắt đầu từ maze ban đầu
            maze_copy = copy.deepcopy(Maze)
            maze_copy[current_state[0]][current_state[1]] = 3
            path_mazes.append(maze_copy)

            while current_state != goal:
                state_key = current_state
                if random.random() < epsilon:
                    action = random.randint(0, 3)
                else:
                    action = q_table[state_key].index(max(q_table[state_key]))

                new_x = current_state[0] + self.Moves[action][0]
                new_y = current_state[1] + self.Moves[action][1]
                new_state = (new_x, new_y)
                if maze_copy[new_x][new_y] == 1:
                    q_table[state_key][action] += -1000000
                    continue
                if self.Check(new_x,new_y):
                    
                    if new_state != goal:
                        if maze_copy[new_x][new_y] == 0:
                            reward = -1
                        if maze_copy[new_x][new_y] == 3:
                            reward = -2
                    else: 
                        reward = 10000000000
                    q_table[state_key][action] += reward + max(q_table[new_state])
                    current_state = new_state
                    way.append(current_state)

                    # lưu lại maze sau khi đi
                    maze_copy = copy.deepcopy(path_mazes[-1])
                    maze_copy[new_x][new_y] = 3
                    path_mazes.append(maze_copy)
                    if maze_copy[new_x][new_y] == 1:
                        break
                    if current_state == goal:
                        return path_mazes
                else:
                    break
        return None
    
    def rangbuoc(self,x,y,new_x,new_y,goal):
        if Manhattan_Heuristic((new_x,new_y),goal) > Manhattan_Heuristic((x,y),goal)+3:
            return True
        return False
    
    def Backtracking(self,Maze,start,goal,path = None,visited = None):
        
        if path is None:
            path = []
        if visited is None:
            visited = set()
        
        x,y = start 
        if start == goal:
            maze = copy.deepcopy(Maze)
            maze[x][y] = 3
            return path + [maze]
        
        visited.add((x,y))
        Maze[x][y] = 3
        
        for dx,dy in self.Moves:
            new_x, new_y = x + dx, y + dy 
            if self.rangbuoc(x,y,new_x,new_y,goal):
                continue
            if self.Check(new_x, new_y) and Maze[new_x][new_y] == 0 and (new_x, new_y) not in visited:
                new_maze = copy.deepcopy(Maze)
                result = self.Backtracking(copy.deepcopy(new_maze),(new_x,new_y),goal,path + [new_maze],visited.copy())
                if result :
                    return result
        return None
    def AND_OR_SEARCH(self,Maze,start,goal,depth = 300):
        visited = set()
        path = self.OR_Search(Maze,start,goal,[],visited,depth)
        return path
    def OR_Search(self,Maze,start,goal,path,visited,depth):
        x,y = start
        if start == goal or depth == 0: 
            maze = copy.deepcopy(Maze)
            maze[x][y] = 3
            return path + [maze]
        visited.add((x,y))
        Maze[x][y] = 3
        
        for dx,dy in self.Moves:
            new_x,new_y = x + dx, y + dy
            if self.Check(new_x,new_y) and Maze[new_x][new_y] == 0 and (new_x,new_y) not in visited:
                lst = []
                if random.random() < 0.9:
                    lst.append((new_x,new_y))
                else:
                    lst.append((x,y))
                new_maze = copy.deepcopy(Maze)
                result = self.AND_Search(copy.deepcopy(new_maze),(new_x,new_y),goal,path + [new_maze],visited.copy(),lst,depth-1)
                if result:
                    return result
        return None
    def AND_Search(self,Maze,start,goal,path,visited,lst,depth):
        result = []
        for step in lst:
            new_visited = visited.copy()
            res = self.OR_Search(Maze,step,goal,path,new_visited,depth-1)
            if not res :
                return None
            result.extend(res)
        return result
        
def draw_way(screen, maze, cell_size):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if int(maze[i][j]) == 3:
                pygame.draw.circle(screen, 'red', (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2), cell_size // 4)