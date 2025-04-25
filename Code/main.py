import pygame
from BanCo import Board
import QuanCo

pygame.init()

screen = pygame.display.set_mode((800,800))
pygame.display.set_caption('Cờ vua AI')
banco_matrix = [
    ['xd', 'nd', 'Td', 'hd', 'vd', 'Td', 'nd', 'xd'],
    ['td', 'td', 'td', 'td', 'td', 'td', 'td', 'td'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['tt', 'tt', 'tt', 'tt', 'tt', 'tt', 'tt', 'tt'],
    ['xt', 'nt', 'Tt', 'ht', 'vt', 'Tt', 'nt', 'xt']
]
banco = Board(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            QuanCo.DiChuyenCo(banco_matrix,event)
            # QuanCo.DiChuyenNgua(banco_matrix,event)
    banco.VeBanCo(QuanCo.nuoc_di_hop_le)
    banco.VeQuanCo(banco_matrix)
    pygame.display.flip()
pygame.display.quit()