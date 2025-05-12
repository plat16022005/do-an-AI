import pygame
import stockfish
import AI
import UI

quan_da_chon = None  # Biến toàn cục để lưu quân đang được chọn
luot = 't'
nuoc_di_hop_le = []


def DiChuyenCo(banco_matrix, event):
    global quan_da_chon, nuoc_di_hop_le, nhapthanh, xe_trang, xe_den, luot
    x, y = event.pos
    col = x // 100
    row = y // 100
    if quan_da_chon is None:
        quan_co = banco_matrix[row][col]
        if quan_co != '-' and quan_co[1] == luot:
            if banco_matrix[row][col] in ['tt', 'td', 'nt', 'nd', 'xt', 'xd', 'Tt', 'Td', 'ht', 'hd', 'vt', 'vd']:
                quan_da_chon = (row, col)
                nuoc_di_hop_le = TimNuocDi(banco_matrix, row, col)  # Xác định nước đi hợp lệ
    else:
        old_row, old_col = quan_da_chon
        quan_co = banco_matrix[old_row][old_col]

        # Nếu nước đi hợp lệ
        if (row, col) in nuoc_di_hop_le:
            banco_tam = [hang.copy() for hang in banco_matrix]
            banco_tam[row][col] = quan_co
            banco_tam[old_row][old_col] = '-'

            # Tìm vị trí vua sau nước đi
            if quan_co[0] == 'v':  # Nếu di chuyển vua
                vua_row, vua_col = row, col
            else:  # Nếu di chuyển quân khác
                vua_row, vua_col = TimViTriVua(banco_tam, quan_co[1])

            # Kiểm tra vua có bị chiếu không
            if not KiemTraChieu(banco_tam, vua_row, vua_col, quan_co[1]):
                # Thực hiện nước đi
                banco_matrix[row][col] = quan_co
                banco_matrix[old_row][old_col] = '-'
                if luot == 't':
                    luot = 'd'
                else:
                    luot = 't'
                # Kiểm tra nếu là nhập thành
                if (quan_co == 'vt' and nhapthanh[0] == True) or (
                        quan_co == 'vd' and nhapthanh[1] == True):  # Vua trắng hoặc đen
                    if abs(col - old_col) == 2:  # Nhập thành
                        # Di chuyển xe
                        if col > old_col and ((quan_co == 'vt' and xe_trang[0] == True) or (
                                quan_co == 'vd' and xe_den[0] == True)):  # Nhập thành phía vua (kingside)
                            banco_matrix[row][col - 1] = banco_matrix[row][7]  # Xe di chuyển đến cạnh vua
                            banco_matrix[row][7] = '-'
                        elif col < old_col and ((quan_co == 'vt' and xe_trang[1] == True) or (
                                quan_co == 'vd' and xe_den[1] == True)):  # Nhập thành phía hậu (queenside)
                            banco_matrix[row][col + 1] = banco_matrix[row][0]  # Xe di chuyển đến cạnh vua
                            banco_matrix[row][0] = '-'
                if quan_co == 'vt' or quan_co == 'xt':
                    if quan_co == 'xt' and xe_trang[0] == True:
                        xe_trang[0] = False
                    elif quan_co == 'xt' and xe_trang[1] == True:
                        xe_trang[1] = False
                    elif quan_co == 'vt' or (xe_trang == [False, False]):
                        nhapthanh[0] = False
                elif quan_co == 'vd' or quan_co == 'xd':
                    if quan_co == 'xd' and xe_den[0] == True:
                        xe_den[0] = False
                    elif quan_co == 'xd' and xe_den[1] == True:
                        xe_den[1] = False
                    elif quan_co == 'vd' or (xe_den == [False, False]):
                        nhapthanh[1] = False
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
    if quan_co == 'vt':  # Vua trắng
        # Nhập thành phía vua (kingside)
        if (banco_matrix[7][5] == '-' and banco_matrix[7][6] == '-' and
                banco_matrix[7][7] == 'xt' and not KiemTraChieu(banco_matrix, 7, 4, 't') and
                not KiemTraChieu(banco_matrix, 7, 5, 't') and not KiemTraChieu(banco_matrix, 7, 6, 't') and nhapthanh[
                    0]):
            nuoc_di_hop_le.append((7, 6))  # Nhập thành phía vua
        # Nhập thành phía hậu (queenside)
        if (banco_matrix[7][1] == '-' and banco_matrix[7][2] == '-' and banco_matrix[7][3] == '-' and
                banco_matrix[7][0] == 'xt' and not KiemTraChieu(banco_matrix, 7, 4, 't') and
                not KiemTraChieu(banco_matrix, 7, 3, 't') and not KiemTraChieu(banco_matrix, 7, 2, 't') and nhapthanh[
                    0]):
            nuoc_di_hop_le.append((7, 2))  # Nhập thành phía hậu
    elif quan_co == 'vd':  # Vua đen
        # Nhập thành phía vua (kingside)
        if (banco_matrix[0][5] == '-' and banco_matrix[0][6] == '-' and
                banco_matrix[0][7] == 'xd' and not KiemTraChieu(banco_matrix, 0, 4, 'd') and
                not KiemTraChieu(banco_matrix, 0, 5, 'd') and not KiemTraChieu(banco_matrix, 0, 6, 'd') and nhapthanh[
                    1]):
            nuoc_di_hop_le.append((0, 6))  # Nhập thành phía vua
        # Nhập thành phía hậu (queenside)
        if (banco_matrix[0][1] == '-' and banco_matrix[0][2] == '-' and banco_matrix[0][3] == '-' and
                banco_matrix[0][0] == 'xd' and not KiemTraChieu(banco_matrix, 0, 4, 'd') and
                not KiemTraChieu(banco_matrix, 0, 3, 'd') and not KiemTraChieu(banco_matrix, 0, 2, 'd') and nhapthanh[
                    1]):
            nuoc_di_hop_le.append((0, 2))  # Nhập thành phía hậu
    return nuoc_di_hop_le


nhapthanh = [True, True]
xe_trang = [True, True]
xe_den = [True, True]


def KiemTraChieu(banco_matrix, vua_row, vua_col, mau_quan):
    """
    Kiểm tra xem vua có đang bị chiếu hay không.
    - banco_matrix: Ma trận bàn cờ.
    - vua_row, vua_col: Vị trí của vua trên bàn cờ.
    - mau_quan: Màu của quân vua ('t' cho trắng, 'd' cho đen).
    """
    doi_phuong = 'd' if mau_quan == 't' else 't'

    # Kiểm tra tấn công từ quân tốt
    huong_tan_cong = -1 if mau_quan == 't' else 1
    for dc in [-1, 1]:
        r, c = vua_row + huong_tan_cong, vua_col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            quan = banco_matrix[r][c]
            if quan == ('t' + doi_phuong):  # Tốt đối phương
                return True

    # Kiểm tra tấn công từ mã (knight)
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in knight_moves:
        r, c = vua_row + dr, vua_col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            quan = banco_matrix[r][c]
            if quan == ('n' + doi_phuong):  # Mã đối phương
                return True

    # Kiểm tra tấn công từ xe, hậu (theo hàng ngang/dọc)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        r, c = vua_row + dr, vua_col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            quan = banco_matrix[r][c]
            if quan != '-':
                if quan[1] == doi_phuong and (quan[0] == 'x' or quan[0] == 'h'):
                    return True
                break
            r += dr
            c += dc

    # Kiểm tra tấn công từ tượng, hậu (theo đường chéo)
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        r, c = vua_row + dr, vua_col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            quan = banco_matrix[r][c]
            if quan != '-':
                if quan[1] == doi_phuong and (quan[0] == 'T' or quan[0] == 'h'):
                    return True
                break
            r += dr
            c += dc

    # Kiểm tra tấn công từ vua đối phương (ô liền kề)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = vua_row + dr, vua_col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                quan = banco_matrix[r][c]
                if quan == ('v' + doi_phuong):
                    return True

    return False


def KiemTraChieuBi(banco_matrix, vua_row, vua_col, mau_quan):
    """
    Kiểm tra xem vua có đang bị chiếu bí hay không.
    - banco_matrix: Ma trận bàn cờ.
    - vua_row, vua_col: Vị trí của vua trên bàn cờ.
    - mau_quan: Màu của quân vua ('t' cho trắng, 'd' cho đen).
    """
    if not KiemTraChieu(banco_matrix, vua_row, vua_col, mau_quan):
        return False

    # 1. Kiểm tra vua có thể di chuyển đến ô không bị chiếu
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = vua_row + dr, vua_col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Kiểm tra ô mới không bị quân đối phương tấn công
                quan_tam = banco_matrix[new_row][new_col]
                if quan_tam == '-' or quan_tam[1] != mau_quan:
                    # Tạo bàn cờ tạm
                    banco_tam = [hang.copy() for hang in banco_matrix]
                    banco_tam[vua_row][vua_col] = '-'
                    banco_tam[new_row][new_col] = 'v' + mau_quan

                    if not KiemTraChieu(banco_tam, new_row, new_col, mau_quan):
                        return False  # Còn nước đi thoát chiếu

    # 2. Kiểm tra có thể chặn chiếu bằng quân khác hoặc ăn quân đang chiếu
    # Tìm quân đang chiếu vua
    for row in range(8):
        for col in range(8):
            if banco_matrix[row][col] != '-' and banco_matrix[row][col][1] == mau_quan:
                nuoc_di_hop_le = TimNuocDi(banco_matrix, row, col)
                for move in nuoc_di_hop_le:
                    banco_tam = [hang.copy() for hang in banco_matrix]
                    banco_tam[move[0]][move[1]] = banco_tam[row][col]
                    banco_tam[row][col] = '-'

                    # Kiểm tra sau khi di chuyển, vua còn bị chiếu không
                    if not KiemTraChieu(banco_tam, vua_row, vua_col, mau_quan):
                        return False  # Còn nước đi thoát chiếu

    return True  # Không còn nước đi thoát chiếu


def KiemTraThangThua(banco_matrix, luot_choi):
    """
    Kiểm tra xem trò chơi đã kết thúc hay chưa (chiếu bí hoặc hòa).
    Trả về:
    - 'thang': Nếu đối phương bị chiếu bí
    - 'thua': Nếu bị chiếu bí
    - 'hoa': Nếu hòa
    - None: Nếu game tiếp tục
    """
    nuocdi = LayTatCaNuocDiHopLe(banco_matrix, luot_choi)
    vua = TimViTriVua(banco_matrix, luot_choi)
    if len(nuocdi) == 0:
        if KiemTraChieu(banco_matrix, vua[0], vua[1], luot_choi):
            if luot_choi == 'd':
                return 'thang'
            elif luot_choi == 't':
                return 'thua'
        else:
            return 'hoa'


def TimViTriVua(banco_matrix, mau_quan):
    """
    Tìm vị trí của vua trên bàn cờ.
    - mau_quan: 't' cho trắng, 'd' cho đen.
    """
    for row in range(8):
        for col in range(8):
            if banco_matrix[row][col] == 'v' + mau_quan:
                return row, col
    return -1, -1  # Trường hợp bất thường (không tìm thấy vua)


def KiemTraSauNuocDi(banco_matrix, luot_choi):
    """
    Kiểm tra chiếu và chiếu bí sau mỗi nước đi.
    - banco_matrix: Ma trận bàn cờ.
    - luot_choi: 't' cho trắng, 'd' cho đen.
    - Trả về:
        - 'thang': Nếu đối phương bị chiếu bí (người chơi hiện tại thắng).
        - 'thua': Nếu người chơi hiện tại bị chiếu bí (người chơi hiện tại thua).
        - 'chieu': Nếu người chơi hiện tại bị chiếu (nhưng chưa thua).
        - None: Nếu trò chơi tiếp tục bình thường.
    """
    # Tìm vị trí vua của người chơi hiện tại
    vua_row, vua_col = TimViTriVua(banco_matrix, luot_choi)
    if vua_row == -1 or vua_col == -1:
        return "Lỗi: Không tìm thấy vua!"

    # Kiểm tra xem người chơi hiện tại có bị chiếu hay không
    if KiemTraChieu(banco_matrix, vua_row, vua_col, luot_choi):
        # Kiểm tra xem có bị chiếu bí hay không
        if KiemTraChieuBi(banco_matrix, vua_row, vua_col, luot_choi):
            return 'thua'  # Người chơi hiện tại bị chiếu bí (thua)
        else:
            return 'chieu'  # Người chơi hiện tại bị chiếu (nhưng chưa thua)
    else:
        # Kiểm tra xem đối phương có bị chiếu bí hay không
        doi_phuong = 'd' if luot_choi == 't' else 't'  # Xác định đối phương
        vua_doi_phuong_row, vua_doi_phuong_col = TimViTriVua(banco_matrix, doi_phuong)
        if KiemTraChieuBi(banco_matrix, vua_doi_phuong_row, vua_doi_phuong_col, doi_phuong):
            return 'thang'  # Đối phương bị chiếu bí (người chơi hiện tại thắng)

    # Nếu không có gì đặc biệt, trò chơi tiếp tục
    return None


def HienThiThongBao(man_hinh, thong_bao):
    """
    Hiển thị thông báo thắng/thua lên màn hình.
    - man_hinh: Đối tượng màn hình pygame.
    - thong_bao: Chuỗi thông báo ("Bạn đã thắng!" hoặc "Bạn đã thua!").
    """
    font = pygame.font.Font(None, 74)  # Chọn font và kích thước
    text = font.render(thong_bao, True, (255, 0, 0))  # Màu đỏ
    text_rect = text.get_rect(center=(400, 300))  # Vị trí giữa màn hình
    man_hinh.blit(text, text_rect)  # Vẽ thông báo lên màn hình
    pygame.display.flip()  # Cập nhật màn hình


def ThietLapBanCo(banco_matrix, luot):
    """
    Thiết lập bàn cờ trong Stockfish.
    - banco_matrix: Ma trận bàn cờ của bạn.
    - luot: Lượt đi hiện tại ('t' hoặc 'd').
    """
    # Chuyển đổi bàn cờ của bạn sang định dạng FEN
    fen = ChuyenDoiSangFEN(banco_matrix, luot)

    # Gửi lệnh position đến Stockfish
    stockfish.stdin.write(f"position fen {fen}\n")
    stockfish.stdin.flush()


def ChuyenDoiSangFEN(banco_matrix, luot):
    """
    Chuyển đổi bàn cờ từ định dạng của bạn sang FEN.
    - banco_matrix: Ma trận 8x8 mô tả bàn cờ.
    - luot: Lượt đi hiện tại ('t' hoặc 'd').
    - Trả về chuỗi FEN.
    """
    quan_co_to_fen = {
        'tt': 'P', 'td': 'p',
        'nt': 'N', 'nd': 'n',
        'xt': 'R', 'xd': 'r',
        'Tt': 'B', 'Td': 'b',
        'ht': 'Q', 'hd': 'q',
        'vt': 'K', 'vd': 'k',
        '-': '1'
    }

    fen_position = []
    for row in banco_matrix:
        fen_row = []
        empty_count = 0
        for cell in row:
            if cell == '-':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row.append(str(empty_count))
                    empty_count = 0
                fen_row.append(quan_co_to_fen[cell])
        if empty_count > 0:
            fen_row.append(str(empty_count))
        fen_position.append(''.join(fen_row))
    fen_position = '/'.join(fen_position)

    fen_turn = 'w' if luot == 't' else 'b'
    fen_castling = 'KQkq'
    fen_en_passant = '-'
    fen_halfmove_clock = '0'
    fen_fullmove_number = '1'

    fen = f"{fen_position} {fen_turn} {fen_castling} {fen_en_passant} {fen_halfmove_clock} {fen_fullmove_number}"
    return fen


def YeuCauNuocDi(stockfish, banco_matrix, luot, thoi_gian=2.0):
    """
    Yêu cầu Stockfish tính toán nước đi tốt nhất.
    - stockfish: Đối tượng Stockfish.
    - banco_matrix: Ma trận bàn cờ của bạn.
    - luot: Lượt đi hiện tại ('t' hoặc 'd').
    - thoi_gian: Thời gian tính toán (giây).
    - Trả về nước đi tốt nhất dưới dạng tuple (start_row, start_col, end_row, end_col).
    """
    # Chuyển đổi bàn cờ sang FEN
    fen = ChuyenDoiSangFEN(banco_matrix, luot)

    # Gửi lệnh position đến Stockfish
    stockfish.stdin.write(f"position fen {fen}\n")
    stockfish.stdin.flush()

    # Gửi lệnh go với thời gian tính toán
    stockfish.stdin.write(f"go movetime {int(thoi_gian * 1000)}\n")
    stockfish.stdin.flush()

    # Đọc phản hồi từ Stockfish
    while True:
        output = stockfish.stdout.readline().strip()
        if output.startswith("bestmove"):
            best_move_uci = output.split()[1]  # Lấy nước đi tốt nhất
            return ChuyenDoiNuocDi(best_move_uci)


def ChuyenDoiNuocDi(best_move_uci):
    """
    Chuyển đổi nước đi từ định dạng UCI sang định dạng của bạn.
    - best_move_uci: Nước đi dưới dạng UCI (ví dụ: "e2e4").
    - Trả về nước đi dưới dạng tuple (start_row, start_col, end_row, end_col).
    """
    start_col = ord(best_move_uci[0]) - ord('a')
    start_row = 8 - int(best_move_uci[1])
    end_col = ord(best_move_uci[2]) - ord('a')
    end_row = 8 - int(best_move_uci[3])
    return (start_row, start_col, end_row, end_col)


May_MCTS = AI.MCTSAI()


# MAY_ALPHA_BETA = AI.AlphaBeta_Prunning()
def AIChoi(stockfish, banco_matrix, luot, luachon, thoi_gian=2.0):
    if stockfish is not None:
        # Sử dụng Stockfish
        fen = ChuyenDoiSangFEN(banco_matrix, luot)
        stockfish.stdin.write(f"position fen {fen}\n")
        stockfish.stdin.flush()
        stockfish.stdin.write(f"go movetime {int(thoi_gian * 1000)}\n")
        stockfish.stdin.flush()

        while True:
            output = stockfish.stdout.readline().strip()
            if output.startswith("bestmove"):
                best_move_uci = output.split()[1]
                return ChuyenDoiNuocDi(best_move_uci)
    else:
        if luachon == 'alpha-beta prunning':
            # Sử dụng AI custom
            is_white = (luot == 't')
            move = AI.ai_make_move(banco_matrix, depth=3, is_white=is_white)
            if move:
                return move
        elif luachon == 'MCTS':
            is_white = (luot == 't')
            move = May_MCTS.ai_make_move(banco_matrix, is_white=is_white)
            if move:
                return move
        elif luachon == 'A*':
            is_white = (luot == 't')
            move = AI.a_star_best_move(banco_matrix, is_white=is_white)
            if move:
                return move
        elif luachon == 'DFS':
            is_white = (luot == 't')
            move = AI.DFS(banco_matrix, is_white=is_white)
            if move:
                return move
        elif luachon == 'Stochastic':
            is_white = (luot == 't')
            move = AI.Stochastic_Hill_Climbing(banco_matrix, is_white=is_white)
            if move:
                return move
        elif luachon == 'Backtracking':
            is_white = (luot == 't')
            _,move = AI.backtracking(banco_matrix, is_white=is_white)
            if move:
                return move
        elif luachon == 'AND-OR':
            is_white = (luot == 't')
            move = AI.AND_OR_SEARCH(banco_matrix, is_white=is_white)
            if move:
                return move
    return None


def CapNhatBanCo(banco_matrix, nuoc_di):
    """
    Cập nhật bàn cờ sau nước đi.
    - banco_matrix: Ma trận bàn cờ.
    - nuoc_di: Nước đi dưới dạng tuple (start_row, start_col, end_row, end_col).
    - Trả về bàn cờ đã được cập nhật.
    """
    if UI.may == 'alpha-beta prunning' or UI.may == 'MCTS':
        start_row, start_col, end_row, end_col = nuoc_di
    else:
        (start_row, start_col), (end_row, end_col) = nuoc_di

    # Kiểm tra nếu nước đi là nhập thành
    if abs(start_col - end_col) == 2 and banco_matrix[start_row][start_col] in ['vt', 'vd']:
        banco_matrix = XuLyNhapThanh(banco_matrix, nuoc_di)
    else:
        # Xử lý nước đi thông thường
        banco_matrix[end_row][end_col] = banco_matrix[start_row][start_col]
        banco_matrix[start_row][start_col] = '-'

    return banco_matrix


def XuLyNhapThanh(banco_matrix, nuoc_di):
    """
    Xử lý nước đi nhập thành.
    - banco_matrix: Ma trận bàn cờ.
    - nuoc_di: Nước đi dưới dạng tuple (start_row, start_col, end_row, end_col).
    - Trả về bàn cờ đã được cập nhật.
    """
    start_row, start_col, end_row, end_col = nuoc_di

    # Kiểm tra nếu nước đi là nhập thành
    if abs(start_col - end_col) == 2 and banco_matrix[start_row][start_col] in ['vt', 'vd']:
        # Di chuyển vua
        banco_matrix[end_row][end_col] = banco_matrix[start_row][start_col]
        banco_matrix[start_row][start_col] = '-'

        # Di chuyển xe
        if end_col > start_col:  # Nhập thành phía vua (kingside)
            banco_matrix[end_row][end_col - 1] = banco_matrix[end_row][7]  # Xe di chuyển đến cạnh vua
            banco_matrix[end_row][7] = '-'
        else:  # Nhập thành phía hậu (queenside)
            banco_matrix[end_row][end_col + 1] = banco_matrix[end_row][0]  # Xe di chuyển đến cạnh vua
            banco_matrix[end_row][0] = '-'

    return banco_matrix


def LayTatCaNuocDiHopLe(banco_matrix, luot):
    """
    Lấy tất cả nước đi hợp lệ cho màu quân hiện tại
    - banco_matrix: ma trận bàn cờ
    - luot: 't' cho trắng, 'd' cho đen
    Trả về: danh sách các nước đi dạng [(start_row, start_col, end_row, end_col), ...]
    """
    tat_ca_nuoc_di = []

    for row in range(8):
        for col in range(8):
            quan_co = banco_matrix[row][col]
            if quan_co != '-' and quan_co[1] == luot:  # Nếu là quân cờ cùng màu lượt đi
                # Lấy các nước đi hợp lệ cho quân cờ này
                cac_nuoc_di = TimNuocDi(banco_matrix, row, col)

                # Kiểm tra từng nước đi có hợp lệ không (không để vua bị chiếu)
                for end_row, end_col in cac_nuoc_di:
                    # Tạo bàn cờ tạm để kiểm tra
                    banco_tam = [hang.copy() for hang in banco_matrix]
                    banco_tam[end_row][end_col] = banco_tam[row][col]
                    banco_tam[row][col] = '-'

                    # Tìm vị trí vua sau nước đi
                    if quan_co[0] == 'v':  # Nếu di chuyển vua
                        vua_row, vua_col = end_row, end_col
                    else:
                        vua_row, vua_col = TimViTriVua(banco_tam, luot)

                    # Nếu vua không bị chiếu thì thêm vào danh sách
                    if not KiemTraChieu(banco_tam, vua_row, vua_col, luot):
                        tat_ca_nuoc_di.append((row, col, end_row, end_col))

    return tat_ca_nuoc_di
