import pygame
import sys

def button(x, y, width, height, text, color, text_color):
    nut = pygame.draw.rect(screen, color, (x, y, width, height), 0, 5)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return nut

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess AI")

background_image = pygame.image.load("Sprite/background.jpg")
background_image = pygame.transform.scale(background_image, (800, 540))  # Resize the image to fit the screen
background_image_rect = background_image.get_rect(center=(400, 400))
style1_image = pygame.image.load("Sprite/vua_den(0).png")
style1_image = pygame.transform.scale(style1_image, (200, 200))  # Resize the image to fit the screen
style1_image_rect = style1_image.get_rect(center=(200, 300))
style2_image = pygame.image.load("Sprite/vua_den(1).png")
style2_image = pygame.transform.scale(style2_image, (200, 200))  # Resize the image to fit the screen
style2_image_rect = style2_image.get_rect(center=(600, 300))
running = True
start = False
choose_mode = False
choose_style = False
mode = ''
may = ''
may1 = ''
may2 = ''
style = 0
# Khởi tạo nút ban đầu
NutStart = None
NutPvP = None
NutPvAI = None
NutAIvAI = None
NutStockfish = None
NutAlphaBeta = None
NutMCTS = None
NutStockfish1 = None
NutAlphaBeta1 = None
NutMCTS1 = None
NutStockfish2 = None
NutAlphaBeta2 = None
NutMCTS2 = None
NutPlay = None
NutStyle1 = None
NutStyle2 = None
def START():
    global running, start, choose_mode, mode, may, may1, may2, style, choose_style
    global NutStart, NutPvP, NutPvAI, NutAIvAI, NutStockfish, NutAlphaBeta, NutMCTS
    global NutStockfish1, NutAlphaBeta1, NutMCTS1, NutStockfish2, NutAlphaBeta2, NutMCTS2, NutPlay, NutStyle1, NutStyle2
    text = 'AI'
    text1 = 'AI 1'
    text2 = 'AI 2'

    while running:
        screen.blit(background_image, background_image_rect)

        if not start:
            NutStart = button(300, 400, 200, 50, "Start", 'darkgray', (255, 255, 255))

        elif start and not choose_style:
            # Chọn style
            Box_1 = pygame.draw.rect(screen, 'lightgray', (100, 200, 200, 200), 0, 5)
            screen.blit(style1_image, style1_image_rect)
            Box_2 = pygame.draw.rect(screen, 'lightgray', (500, 200, 200, 200), 0, 5)
            screen.blit(style2_image, style2_image_rect)
            font = pygame.font.Font(None, 48)
            font2 = pygame.font.Font(None, 52)
            text_surface = font.render("Choose style", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(400, 150))
            screen.blit(text_surface, text_rect)
            text_normal = font.render("Normal", True, (255, 255, 255))
            text_normal_border = font2.render("Normal", True, (0, 0, 0))
            text_normal_rect = text_normal.get_rect(center=(200, 450))
            text_normal_rect_border = text_normal_border.get_rect(center=(200, 450))
            screen.blit(text_normal_border, text_normal_rect_border)
            screen.blit(text_normal, text_normal_rect)
            text_anime = font.render("Anime", True, (255, 255, 255))
            text_anime_border = font2.render("Anime", True, (0, 0, 0))
            text_anime_rect = text_anime.get_rect(center=(600, 450))
            text_anime_rect_border = text_anime_border.get_rect(center=(600, 450))
            screen.blit(text_anime_border, text_anime_rect_border)
            screen.blit(text_anime, text_anime_rect)
            NutStyle1 = button(100, 500, 200, 50, "Choose", 'darkgray', (255, 255, 255))
            NutStyle2 = button(500, 500, 200, 50, "Choose", 'darkgray', (255, 255, 255))

        elif start and choose_style and not choose_mode:
            # Chọn chế độ chơi
            font = pygame.font.Font(None, 48)
            text_surface = font.render(f"Choose mode", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(400, 200))
            screen.blit(text_surface, text_rect)
            NutPvP = button(300, 300, 200, 50, "P vs P", 'darkgray', (255, 255, 255))
            NutPvAI = button(300, 400, 200, 50, "P vs AI", 'darkgray', (255, 255, 255))
            NutAIvAI = button(300, 500, 200, 50, "AI vs AI", 'darkgray', (255, 255, 255))

        elif choose_style and choose_mode:
            # Nếu là P vs AI → chọn 1 AI
            if mode == 'P vs AI':
                font = pygame.font.Font(None, 48)
                font2 = pygame.font.Font(None, 56)
                font3 = pygame.font.Font(None, 60)
                text_surface = font.render(f"Choose AI", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(400, 200))
                screen.blit(text_surface, text_rect)
                text_AI = font2.render(text, True, (255, 255, 255))
                text_AI_border = font3.render(text, True, (0, 0, 0))
                text_rect_AI_border = text_AI_border.get_rect(center=(400, 250))
                text_rect_AI = text_AI.get_rect(center=(400, 250))
                screen.blit(text_AI_border, text_rect_AI_border)
                screen.blit(text_AI, text_rect_AI)
                NutStockfish = button(300, 300, 200, 50, "Stockfish", 'darkblue', (255, 255, 255))
                NutAlphaBeta = button(300, 400, 200, 50, "Alpha-Beta", 'blue', (255, 255, 255))
                NutMCTS = button(300, 500, 200, 50, "MCTS", 'lightblue', (255, 255, 255))

            elif mode == 'AI vs AI':
                font = pygame.font.Font(None, 48)
                text_surface = font.render("Choose AI", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(400, 200))
                screen.blit(text_surface, text_rect)
                font2 = pygame.font.Font(None, 56)
                font3 = pygame.font.Font(None, 60)
                text_VS = font2.render("VS", True, (255, 255, 255))
                text_VS_border = font3.render("VS", True, (0, 0, 0))
                screen.blit(text_VS_border, text_VS_border.get_rect(center=(400, 400)))
                screen.blit(text_VS, text_VS.get_rect(center=(400, 400)))

                # AI 1
                NutStockfish1 = button(100, 300, 200, 50, "Stockfish", 'darkblue', (255, 255, 255))
                NutAlphaBeta1 = button(100, 400, 200, 50, "Alpha-Beta", 'blue', (255, 255, 255))
                NutMCTS1 = button(100, 500, 200, 50, "MCTS", 'lightblue', (255, 255, 255))
                screen.blit(font3.render(text1, True, (0, 0, 0)), font3.render(text1, True, (0, 0, 0)).get_rect(center=(200, 250)))
                screen.blit(font2.render(text1, True, (255, 255, 255)), font2.render(text1, True, (255, 255, 255)).get_rect(center=(200, 250)))

                # AI 2
                NutStockfish2 = button(500, 300, 200, 50, "Stockfish", 'darkblue', (255, 255, 255))
                NutAlphaBeta2 = button(500, 400, 200, 50, "Alpha-Beta", 'blue', (255, 255, 255))
                NutMCTS2 = button(500, 500, 200, 50, "MCTS", 'lightblue', (255, 255, 255))
                screen.blit(font3.render(text2, True, (0, 0, 0)), font3.render(text2, True, (0, 0, 0)).get_rect(center=(600, 250)))
                screen.blit(font2.render(text2, True, (255, 255, 255)), font2.render(text2, True, (255, 255, 255)).get_rect(center=(600, 250)))

            NutPlay = button(300, 700, 200, 50, "Play", 'darkgray', (255, 255, 255))

        # Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NutStart and NutStart.collidepoint(event.pos):
                    start = True
                if start and not choose_style:
                    if NutStyle1 and NutStyle1.collidepoint(event.pos):
                        choose_style = True
                        style = 0
                    if NutStyle2 and NutStyle2.collidepoint(event.pos):
                        choose_style = True
                        style = 1
                elif choose_style and not choose_mode:
                    if NutPvP and NutPvP.collidepoint(event.pos):
                        choose_mode = True
                        mode = 'P vs P'
                        running = False
                    elif NutPvAI and NutPvAI.collidepoint(event.pos):
                        choose_mode = True
                        mode = 'P vs AI'
                    elif NutAIvAI and NutAIvAI.collidepoint(event.pos):
                        choose_mode = True
                        mode = 'AI vs AI'
                elif choose_style and choose_mode:
                    if mode == 'P vs AI':
                        if NutStockfish and NutStockfish.collidepoint(event.pos):
                            may = 'Stockfish'
                            text = 'Stockfish'
                        if NutAlphaBeta and NutAlphaBeta.collidepoint(event.pos):
                            may = 'alpha-beta prunning'
                            text = 'Alpha-Beta'
                        if NutMCTS and NutMCTS.collidepoint(event.pos):
                            may = 'MCTS'
                            text = 'MCTS'
                    if mode == 'AI vs AI':
                        if NutStockfish1 and NutStockfish1.collidepoint(event.pos):
                            may1 = 'Stockfish'
                            text1 = 'Stockfish'
                        if NutAlphaBeta1 and NutAlphaBeta1.collidepoint(event.pos):
                            may1 = 'alpha-beta prunning'
                            text1 = 'Alpha-Beta'
                        if NutMCTS1 and NutMCTS1.collidepoint(event.pos):
                            may1 = 'MCTS'
                            text1 = 'MCTS'
                        if NutStockfish2 and NutStockfish2.collidepoint(event.pos):
                            may2 = 'Stockfish'
                            text2 = 'Stockfish'
                        if NutAlphaBeta2 and NutAlphaBeta2.collidepoint(event.pos):
                            may2 = 'alpha-beta prunning'
                            text2 = 'Alpha-Beta'
                        if NutMCTS2 and NutMCTS2.collidepoint(event.pos):
                            may2 = 'MCTS'
                            text2 = 'MCTS'
                    if NutPlay and NutPlay.collidepoint(event.pos):
                        if mode == 'P vs AI' and text != 'AI':
                            running = False
                        elif mode == 'AI vs AI' and text1 != 'AI 1' and text2 != 'AI 2':
                            running = False
        
        pygame.display.flip()