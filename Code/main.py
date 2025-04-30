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
            ket_qua = QuanCo.KiemTraSauNuocDi(banco_matrix, QuanCo.luot)
            if ket_qua == 'thang':
                QuanCo.HienThiThongBao(screen, "You Win!")
                pygame.time.wait(3000)  # Hiển thị thông báo trong 3 giây
                running = False  # Kết thúc trò chơi
            elif ket_qua == 'thua':
                QuanCo.HienThiThongBao(screen, "You Lose!")
                pygame.time.wait(3000)  # Hiển thị thông báo trong 3 giây
                running = False  # Kết thúc trò chơi
            elif ket_qua == 'chieu':
                print("Bạn đang bị chiếu! Hãy thoát khỏi chiếu.")
    banco.VeBanCo(QuanCo.nuoc_di_hop_le)
    banco.VeQuanCo(banco_matrix)

    pygame.display.flip()
pygame.display.quit()