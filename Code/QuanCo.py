import pygame

quan_da_chon = None  # Biến toàn cục để lưu quân đang được chọn
nuoc_di_hop_le = []


def DiChuyenCo(banco_matrix, event):
    global quan_da_chon, nuoc_di_hop_le
    x, y = event.pos
    col = x // 100
    row = y // 100
    if quan_da_chon is None:
        if banco_matrix[row][col] in ['tt', 'td', 'nt', 'nd', 'xt', 'xd', 'Tt', 'Td', 'ht', 'hd', 'vt', 'vd']:
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

    elif quan_co == 'nt':
        nuoc_di_hop_le_cua_quan_ngua = [
            (row - 2, col - 1), (row - 2, col + 1),
            (row + 2, col - 1), (row + 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2),
            (row + 1, col - 2), (row + 1, col + 2)
        ]
        for (i, j) in nuoc_di_hop_le_cua_quan_ngua:
            if 0 <= i <= 7 and 0 <= j <= 7:
                if banco_matrix[i][j] == '-' or banco_matrix[i][j][1] == 'd':
                    nuoc_di_hop_le.append((i, j))

    elif quan_co == 'nd':
        nuoc_di_hop_le_cua_quan_ngua = [
            (row - 2, col - 1), (row - 2, col + 1),
            (row + 2, col - 1), (row + 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2),
            (row + 1, col - 2), (row + 1, col + 2)
        ]
        for (i, j) in nuoc_di_hop_le_cua_quan_ngua:
            if 0 <= i <= 7 and 0 <= j <= 7:
                if banco_matrix[i][j] == '-' or banco_matrix[i][j][1] == 't':
                    nuoc_di_hop_le.append((i, j))
    elif quan_co == 'xt':
        nuoc_di_hop_le_cua_quan_xe = []
        x = []
        for i in range(1, 8):
            x.append((row + i, col))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1, 8):
            x.append((row - i, col))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1, 8):
            x.append((row, col + i))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1, 8):
            x.append((row, col - i))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        for z in nuoc_di_hop_le_cua_quan_xe:
            for (i, j) in z:
                if 0 <= i <= 7 and 0 <= j <= 7:
                    if banco_matrix[i][j] == '-':
                        nuoc_di_hop_le.append((i, j))
                    elif banco_matrix[i][j][1] == 'd':
                        nuoc_di_hop_le.append((i, j))
                        break
                    elif banco_matrix[i][j][1] == 't':
                        break
    elif quan_co == 'xd':
        nuoc_di_hop_le_cua_quan_xe = []
        x = []
        for i in range(1, 8):
            x.append((row + i, col))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1, 8):
            x.append((row - i, col))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1, 8):
            x.append((row, col + i))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1, 8):
            x.append((row, col - i))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        for z in nuoc_di_hop_le_cua_quan_xe:
            for (i, j) in z:
                if 0 <= i <= 7 and 0 <= j <= 7:
                    if banco_matrix[i][j] == '-':
                        nuoc_di_hop_le.append((i, j))
                    elif banco_matrix[i][j][1] == 't':
                        nuoc_di_hop_le.append((i, j))
                        break
                    elif banco_matrix[i][j][1] == 'd':
                        break
    elif quan_co == 'Tt':
        moves = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        for i, j in moves:
            new_row = row
            new_col = col
            for k in range(1, 8):
                new_row = new_row + i
                new_col = new_col + j
                if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                    if banco_matrix[new_row][new_col] == '-':
                        nuoc_di_hop_le.append((new_row, new_col))
                    elif banco_matrix[new_row][new_col][1] == 'd':
                        nuoc_di_hop_le.append((new_row, new_col))
                        break
                    elif banco_matrix[new_row][new_col][1] == 't':
                        break
    elif quan_co == 'Td':
        moves = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        for i, j in moves:
            new_row = row
            new_col = col
            for k in range(1, 8):
                new_row = new_row + i
                new_col = new_col + j
                if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                    if banco_matrix[new_row][new_col] == '-':
                        nuoc_di_hop_le.append((new_row, new_col))
                    elif banco_matrix[new_row][new_col][1] == 't':
                        nuoc_di_hop_le.append((new_row, new_col))
                        break
                    elif banco_matrix[new_row][new_col][1] == 'd':
                        break
    elif quan_co == 'ht':
        moves = [(-1, -1), (1, 1), (-1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)]
        for i, j in moves:
            new_row = row
            new_col = col
            for k in range(1, 8):
                new_row = new_row + i
                new_col = new_col + j
                if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                    if banco_matrix[new_row][new_col] == '-':
                        nuoc_di_hop_le.append((new_row, new_col))
                    elif banco_matrix[new_row][new_col][1] == 'd':
                        nuoc_di_hop_le.append((new_row, new_col))
                        break
                    elif banco_matrix[new_row][new_col][1] == 't':
                        break
    elif quan_co == 'hd':
        moves = [(-1, -1), (1, 1), (-1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)]
        for i, j in moves:
            new_row = row
            new_col = col
            for k in range(1, 8):
                new_row = new_row + i
                new_col = new_col + j
                if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                    if banco_matrix[new_row][new_col] == '-':
                        nuoc_di_hop_le.append((new_row, new_col))
                    elif banco_matrix[new_row][new_col][1] == 't':
                        nuoc_di_hop_le.append((new_row, new_col))
                        break
                    elif banco_matrix[new_row][new_col][1] == 'd':
                        break
    elif quan_co == 'vt':
        moves = [(-1, -1), (1, 1), (-1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)]
        for (i, j) in moves:
            new_row = row + i
            new_col = col + j
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                if banco_matrix[new_row][new_col] == '-':
                    nuoc_di_hop_le.append((new_row, new_col))
                elif banco_matrix[new_row][new_col][1] == 'd':
                    nuoc_di_hop_le.append((new_row, new_col))
                    continue
                elif banco_matrix[new_row][new_col][1] == 't':
                    continue
    elif quan_co == 'vd':
        moves = [(-1, -1), (1, 1), (-1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)]
        for (i, j) in moves:
            new_row = row + i
            new_col = col + j
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                if banco_matrix[new_row][new_col] == '-':
                    nuoc_di_hop_le.append((new_row, new_col))
                elif banco_matrix[new_row][new_col][1] == 't':
                    nuoc_di_hop_le.append((new_row, new_col))
                    continue
                elif banco_matrix[new_row][new_col][1] == 'd':
                    continue
    return nuoc_di_hop_le