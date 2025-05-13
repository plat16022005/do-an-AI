import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((1200, 810))
START = False
choose_maze = False
choose_size = False
size = 27
maze = ''
background_image = pygame.image.load("find-way/background.jpg")
background_image = pygame.transform.scale(background_image, (1200, 810))
background_image_rect = background_image.get_rect(center = (600, 405))
def button(x, y, width, height, text, color, text_color):
    nut = pygame.draw.rect(screen, color, (x, y, width, height), 0, 5)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return nut
running = True
def VeUI():
    global START, running, maze, size, choose_size
    text = "Welcome to the FIND WAY"
    
    while running:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text_surface = font.render(text, True, (255, 255, 255))
        text_surface_border = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(600, 100))
        text_rect_border = text_surface_border.get_rect(center=(602, 102))
        
        screen.blit(background_image, background_image_rect)
        screen.blit(text_surface_border, text_rect_border)
        screen.blit(text_surface, text_rect)

        # Tạo nút
        if not START and not choose_size:
            BTN_START = button(500, 400, 250, 50, "START", 'blue', (255, 255, 255))
        elif START:
            if choose_size:
                text = "Choose the maze"
                BTN_BFS = button(500, 400, 250, 50, "BFS", 'blue', (255, 255, 255))
                BTN_DFS = button(500, 470, 250, 50, "DFS", 'blue', (255, 255, 255))
                BTN_PRIM = button(500, 540, 250, 50, "PRIM", 'blue', (255, 255, 255))
            else:
                text = "Choose size"
                BTN_9x9 = button(500,400,250,50, "9 x 9", 'blue', (255,255,255))
                BTN_27x27 = button(500,470,250,50, "27 x 27", 'blue', (255,255,255))
                BTN_81x81 = button(500,540,250,50, "81 x 81", 'blue', (255,255,255))

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if not START:
                    if BTN_START.collidepoint(mouse_x, mouse_y):
                        START = True
                else:
                    if choose_size:
                        if BTN_BFS.collidepoint(mouse_x, mouse_y):
                            maze = 'bfs'
                            running = False
                        elif BTN_DFS.collidepoint(mouse_x, mouse_y):
                            maze = 'dfs'
                            running = False
                        elif BTN_PRIM.collidepoint(mouse_x, mouse_y):
                            maze = 'prim'
                            running = False
                    else:
                        if BTN_9x9.collidepoint(mouse_x,mouse_y):
                            size = 9
                            choose_size = True
                        elif BTN_27x27.collidepoint(mouse_x,mouse_y):
                            size = 27
                            choose_size = True
                        elif BTN_81x81.collidepoint(mouse_x,mouse_y):
                            size = 81
                            choose_size = True

        pygame.display.flip()
