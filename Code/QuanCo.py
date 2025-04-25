import pygame

quan_da_chon = None  # Biến toàn cục để lưu quân đang được chọn
nuoc_di_hop_le = []
def DiChuyenCo(banco_matrix, event):
    global quan_da_chon, nuoc_di_hop_le
    x, y = event.pos
    col = x // 100
    row = y // 100
    if quan_da_chon is None:
        if banco_matrix[row][col] in ['tt', 'td']:  
            quan_da_chon = (row, col)
            nuoc_di_hop_le = TimNuocDi(banco_matrix, row, col)  # Xác định nước đi hợp lệ
    else:
        old_row, old_col = quan_da_chon
        quan_co = banco_matrix[old_row][old_col]

        # Nếu nước đi hợp lệ
        if (row, col) in nuoc_di_hop_le:
            banco_matrix[row][col] = quan_co  # Di chuyển hoặc ăn quân
            banco_matrix[old_row][old_col] = '-'  # Xóa quân cũ

        # Hủy chọn sau khi di chuyển hoặc click ra ngoài
        quan_da_chon = None
        nuoc_di_hop_le = []
def TimNuocDi(banco_matrix, row, col):
    """ Tìm nước đi hợp lệ cho tất cả các quân cờ """
    nuoc_di_hop_le = []
    quan_co = banco_matrix[row][col]

    if quan_co == 'tt':  # Tốt trắng đi lên
        # Đi thẳng nếu ô trước mặt trống
        if row > 0 and banco_matrix[row - 1][col] == '-':  
            nuoc_di_hop_le.append((row - 1, col))
            if row == 6 and banco_matrix[row - 2][col] == '-':
                nuoc_di_hop_le.append((row - 2, col))

        # Kiểm tra nước đi chéo để ăn quân đen
        if row > 0 and col > 0 and banco_matrix[row - 1][col - 1] != '-' and banco_matrix[row - 1][col - 1][1] == 'd':
            nuoc_di_hop_le.append((row - 1, col - 1))
        if row > 0 and col < 7 and banco_matrix[row - 1][col + 1] != '-' and banco_matrix[row - 1][col + 1][1] == 'd':
            nuoc_di_hop_le.append((row - 1, col + 1))

    elif quan_co == 'td':  # Tốt đen đi xuống
        # Đi thẳng nếu ô trước mặt trống
        if row < 7 and banco_matrix[row + 1][col] == '-':  
            nuoc_di_hop_le.append((row + 1, col))
            if row == 1 and banco_matrix[row + 2][col] == '-':
                nuoc_di_hop_le.append((row + 2, col))

        # Kiểm tra nước đi chéo để ăn quân trắng
        if row < 7 and col > 0 and banco_matrix[row + 1][col - 1] != '-' and banco_matrix[row + 1][col - 1][1] == 't':
            nuoc_di_hop_le.append((row + 1, col - 1))
        if row < 7 and col < 7 and banco_matrix[row + 1][col + 1] != '-' and banco_matrix[row + 1][col + 1][1] == 't':
            nuoc_di_hop_le.append((row + 1, col + 1))
    return nuoc_di_hop_le