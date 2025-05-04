import pygame
from BanCo import Board
import QuanCo
import subprocess
import threading
import queue
import AI
# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Cờ vua AI')

# Khởi tạo Stockfish
STOCKFISH_PATH = "D:\\Đồ án AI\\stockfish\\stockfish-windows-x86-64-avx2"
stockfish = subprocess.Popen(
    STOCKFISH_PATH,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    bufsize=1
)

# Gửi lệnh khởi tạo UCI
stockfish.stdin.write("uci\n")
stockfish.stdin.flush()

# Đọc phản hồi từ Stockfish
while True:
    output = stockfish.stdout.readline().strip()
    print(output)
    if output == "uciok":
        break

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
# banco_matrix = [
#     ['vd', '-', '-', '-', '-', 'Td', '-', '-'],
#     ['-', 'td', '-', 'td', 'td', 'td', 'td', 'xd'],
#     ['-', 'tt', '-', 'td', '-', '-', '-', 'td'],
#     ['-', '-', '-', 'tt', '-', 'tt', '-', '-'],
#     ['-', '-', 'tt', 'vt', 'tt', '-', '-', 'tt'],
#     ['-', '-', '-', 'Tt', '-', '-', 'tt', '-'],
#     ['-', '-', 'nt', '-', '-', '-', '-', '-'],
#     ['-', '-', 'hd', '-', '-', '-', '-', '-']
# ]
banco = Board(screen)

ai_result_queue1 = queue.Queue()
ai_thread1 = None

# Biến toàn cục để lưu trữ kết quả từ luồng AI
ai_result_queue2 = queue.Queue()
ai_thread2 = None
running = True

# Hàm để chạy AI trên luồng riêng
def AIChoiThread(stockfish, banco_matrix, luot, luachon, result_queue):
    nuoc_di = QuanCo.AIChoi(stockfish, banco_matrix, luot, luachon)
    if nuoc_di:
        result_queue.put(nuoc_di)

# Vòng lặp chính
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if QuanCo.luot == 't':
                QuanCo.DiChuyenCo(banco_matrix, event)
                
                # Vẽ lại bàn cờ với nước đi cuối cùng
                banco.VeBanCo(QuanCo.nuoc_di_hop_le)
                banco.VeQuanCo(banco_matrix)
                pygame.display.flip()
                
                # Hiển thị nước đi trong 1 giây trước khi kiểm tra kết quả
                
                ket_qua = QuanCo.KiemTraThangThua(banco_matrix, QuanCo.luot)
                if ket_qua == 'thang':
                    QuanCo.HienThiThongBao(screen, "wHITE WIN!")
                    running = False
                elif ket_qua == 'thua':
                    QuanCo.HienThiThongBao(screen, "BLACK win!")
                    running = False
                elif ket_qua == 'chieu':
                    print("Bạn đang bị chiếu! Hãy thoát khỏi chiếu.")
            # if QuanCo.luot == 't' and (ai_thread1 is None or not ai_thread1.is_alive()):
            #     choice = 'alpha-beta prunning'
            #     ai_thread1 = threading.Thread(target=AIChoiThread, args=(None,banco_matrix, QuanCo.luot, choice,ai_result_queue1))
            #     ai_thread1.start()
                # Sau khi quân trắng đi xong, bắt đầu luồng AI cho quân đen
            # if QuanCo.luot == 'd' and (ai_thread2 is None or not ai_thread2.is_alive()):
            #     ai_thread2 = threading.Thread(target=AIChoiThread, args=(stockfish, banco_matrix, QuanCo.luot, ai_result_queue2))
            #     ai_thread2.start()
            if QuanCo.luot == 'd' and (ai_thread2 is None or not ai_thread2.is_alive()):
                choice = 'alpha-beta prunning'
                ai_thread2 = threading.Thread(target=AIChoiThread, args=(None, banco_matrix, QuanCo.luot, choice,ai_result_queue2))
                ai_thread2.start()
    if ai_thread1 and not ai_thread1.is_alive():
        if not ai_result_queue1.empty():
            nuoc_di = ai_result_queue1.get()
            banco_matrix = QuanCo.CapNhatBanCo(banco_matrix, nuoc_di)
            
            banco.VeBanCo(QuanCo.nuoc_di_hop_le)
            banco.VeQuanCo(banco_matrix)
            pygame.display.flip()
            QuanCo.luot = 'd'  # Đổi lượt về quân trắng

            # Kiểm tra kết quả sau nước đi của quân đen
            ket_qua = QuanCo.KiemTraSauNuocDi(banco_matrix, QuanCo.luot)
            if ket_qua == 'thang':
                QuanCo.HienThiThongBao(screen, "WHITE win!")
                pygame.time.wait(5000)
                running = False
            elif ket_qua == 'thua':
                QuanCo.HienThiThongBao(screen, "BLACK WIN!")
                pygame.time.wait(5000)
                running = False
            elif ket_qua == 'chieu':
                print("Bạn đang bị chiếu!")
    # Kiểm tra xem AI đã hoàn thành nước đi chưa
    if ai_thread2 and not ai_thread2.is_alive():
        if not ai_result_queue2.empty():
            nuoc_di = ai_result_queue2.get()
            banco_matrix = QuanCo.CapNhatBanCo(banco_matrix, nuoc_di)
            
            # Vẽ lại bàn cờ với nước đi cuối cùng
            banco.VeBanCo(QuanCo.nuoc_di_hop_le)
            banco.VeQuanCo(banco_matrix)
            pygame.display.flip()
            
            # Hiển thị nước đi trong 1 giây trước khi kiểm tra kết quả
            
            QuanCo.luot = 't'  # Đổi lượt về quân trắng

            # Kiểm tra kết quả sau nước đi của quân đen
            ket_qua = QuanCo.KiemTraThangThua(banco_matrix, 't')
            if ket_qua == 'thang':
                QuanCo.HienThiThongBao(screen, "White Win!")
                pygame.time.wait(5000)
                running = False
            elif ket_qua == 'thua':
                QuanCo.HienThiThongBao(screen, "Black Win!")
                pygame.time.wait(5000)
                running = False
            elif ket_qua == 'chieu':
                print("Bạn đang bị chiếu!")

    # Vẽ bàn cờ và các quân cờ
    banco.VeBanCo(QuanCo.nuoc_di_hop_le)
    banco.VeQuanCo(banco_matrix)
    pygame.display.flip()

# Đóng Stockfish và Pygame
stockfish.stdin.write("quit\n")
stockfish.stdin.flush()
stockfish.terminate()
pygame.quit()