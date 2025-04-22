import pygame

class Board():
    def __init__(self, screen):
        self.screen = screen
    def VeBanCo(self):
        self.screen.fill('brown')
        for i in range(32):
            cot = i % 4
            dong = i // 4
            if dong % 2 == 0:
                pygame.draw.rect(self.screen, 'light gray', [600 - (cot*200), dong*100, 100, 100])
            else:
                pygame.draw.rect(self.screen, 'light gray', [700 - (cot*200), dong*100, 100, 100])
        pygame.display.flip()