import pygame
from BanCo import Board

pygame.init()

screen = pygame.display.set_mode((800,800))
pygame.display.set_caption('Cờ vua AI')
banco_matrix = [
    ['xt', 'nt', 'Tt', 'ht', 'vt', 'Tt', 'nt', 'xt'],
    ['tt', 'tt', 'tt', 'tt', 'tt', 'tt', 'tt', 'tt'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['td', 'td', 'td', 'td', 'td', 'td', 'td', 'td'],
    ['xd', 'nd', 'Td', 'hd', 'vd', 'Td', 'nd', 'xd']
]
banco = Board(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    banco.VeBanCo()
    banco.VeQuanCo(banco_matrix)
    # pygame.display.update()
    pygame.display.flip()
pygame.display.quit()