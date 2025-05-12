import pygame
import MakeMaze
import AI
import UI

pygame.init()

# Khởi tạo màn hình
screen = pygame.display.set_mode((1200, 810))


# Khởi tạo AI với kích thước mê cung 27x27, mỗi ô 30px
ai = AI.Algorithm(screen, MakeMaze.m, MakeMaze.n, 30)

# Tìm đường đi từ vị trí bắt đầu đến goal
# Biến điều khiển
index = 0
index_ai = 0
maked_maze = False
drawn_path = False
done = False
choose = False
clock = pygame.time.Clock()
maze_type = ''
UI.VeUI()
if UI.maze == 'bfs':
    path = MakeMaze.bfs(1,1)
elif UI.maze == 'dfs':
    path = MakeMaze.dfs(1,1)
elif UI.maze == 'prim':
    path = MakeMaze.prim_maze(27,27,1,1)

goal_pos = MakeMaze.random_goal(path[-1])
start_pos = [1, 1]
MakeMaze.add_extra_connections(path[-1], 0.1)
running = True
def button(x, y, width, height, text, color, text_color):
    nut = pygame.draw.rect(screen, color, (x, y, width, height), 0, 5)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return nut
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if Button_DFS.collidepoint(mouse_x, mouse_y):
                path_ai = ai.DFS(path[-1], start_pos, goal_pos)
                choose = True
                done = False
                drawn_path = False
                index_ai = 0
            elif Button_BFS.collidepoint(mouse_x, mouse_y):
                path_ai = ai.BFS(path[-1], start_pos, goal_pos)
                choose = True
                done = False
                drawn_path = False
                index_ai = 0
            elif Button_Astar.collidepoint(mouse_x, mouse_y):
                path_ai = ai.A_Star_Search(path[-1], start_pos, goal_pos)
                choose = True
                done = False
                drawn_path = False
                index_ai = 0
            elif Button_Beam.collidepoint(mouse_x, mouse_y):
                path_ai = ai.Beam_Search(path[-1], start_pos, goal_pos)
                choose = True
                done = False
                drawn_path = False
                index_ai = 0
            elif Button_Steepest.collidepoint(mouse_x, mouse_y):
                path_ai = ai.Steepest_Ascent_Hill_Climbing(path[-1], start_pos, goal_pos)
                choose = True
                done = False
                drawn_path = False
                index_ai = 0
            elif Button_QLearning.collidepoint(mouse_x, mouse_y):
                path_ai = ai.q_study(path[-1], start_pos, goal_pos)
                choose = True
                done = False
                drawn_path = False
                index_ai = 0
            elif Button_Result.collidepoint(mouse_x, mouse_y):
                if path_ai:
                    index_ai = len(path_ai) - 1
            elif Button_Random_Goal.collidepoint(mouse_x, mouse_y):
                if choose == False:
                    goal_pos = MakeMaze.random_goal(path[-1])
            elif Button_Backtracking.collidepoint(mouse_x, mouse_y):
                path_ai = ai.Backtracking(path[-1], start_pos, goal_pos)
                choose = True
                done = False
                drawn_path = False
                index_ai = 0
            elif Button_AND_OR_SEARCH.collidepoint(mouse_x, mouse_y):
                path_ai = ai.AND_OR_SEARCH(path[-1], start_pos, goal_pos)
                choose = True
                done = False
                drawn_path = False
                index_ai = 0

    screen.fill('white')

    # Vẽ vị trí bắt đầu
    pygame.draw.rect(screen, 'red', (start_pos[0]*30, start_pos[1]*30, 30, 30))

    # Vẽ mê cung theo từng bước
    MakeMaze.draw_maze(screen, path[index])
    Button_DFS = button(820, 50, 160, 50, "DFS", 'blue', 'white')
    Button_BFS = button(820, 150, 160, 50, "BFS", 'blue', 'white')
    Button_Astar = button(820, 250, 160, 50, "A*", 'blue', 'white')
    Button_Beam = button(820, 350, 160, 50, "Beam", 'blue', 'white')
    Button_Steepest = button(820, 450, 160, 50, "Steepest", 'blue', 'white')
    Button_QLearning = button(820, 550, 160, 50, "Q-Learning", 'blue', 'white')
    Button_Backtracking = button(820, 650, 160, 50, "Backtracking", 'blue', 'white')
    Button_AND_OR_SEARCH = button(820, 750, 160, 50, "AND-OR", 'blue', 'white')
    
    Button_Result = button(1000, 50, 160, 50, "Result", 'red', 'white')
    Button_Random_Goal = button(1000, 250, 160, 50, "Random Goal", 'green', 'white')
    # Tăng index cho đến khi vẽ hết
    if index < len(path) - 1 and not maked_maze:
        index += 1
    else:
        maked_maze = True
    if choose:
        if maked_maze and not done:
            pygame.draw.rect(screen, 'green', (goal_pos[1] * 30, goal_pos[0] * 30, 30, 30))
            # Vẽ đường đi của AI
            if index_ai < len(path_ai) - 1 and not drawn_path:
                AI.draw_way(screen, path_ai[index_ai], 30)
                index_ai += 1
            else:
                drawn_path = True
                done = True
        # Vẽ mê cung đã hoàn thành
        if done:
            MakeMaze.draw_maze(screen, path[-1])
            AI.draw_way(screen, path_ai[-1], 30)
            pygame.time.delay(1000)
    else:
        # Vẽ mê cung đã hoàn thành
        MakeMaze.draw_maze(screen, path[-1])
        if maked_maze:
            pygame.draw.rect(screen, 'green', (goal_pos[1] * 30, goal_pos[0] * 30, 30, 30))
    pygame.display.flip()
    clock.tick(10)  # Giới hạn tốc độ khung hình

pygame.quit()
