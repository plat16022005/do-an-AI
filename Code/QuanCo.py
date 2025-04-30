
import pygame

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
            if banco_matrix[row][col] in ['tt', 'td', 'nt', 'nd', 'xt','xd','Tt','Td','ht','hd','vt','vd']:  
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

            # Kiểm tra xem vua có bị chiếu sau nước đi này không
            vua_row, vua_col = TimViTriVua(banco_tam, quan_co[1])  # Tìm vị trí vua
            if not KiemTraChieu(banco_tam, vua_row, vua_col, quan_co[1]):
                # Nếu không bị chiếu, thực hiện nước đi
                banco_matrix[row][col] = quan_co
                banco_matrix[old_row][old_col] = '-'
                if luot == 't':
                    luot = 'd'
                else:
                    luot = 't'
                # Kiểm tra nếu là nhập thành
                if (quan_co == 'vt' and nhapthanh[0] == True) or (quan_co == 'vd' and nhapthanh[1] == True):  # Vua trắng hoặc đen
                    if abs(col - old_col) == 2:  # Nhập thành
                        # Di chuyển xe
                        if col > old_col and ((quan_co == 'vt' and xe_trang[0] == True) or (quan_co == 'vd' and xe_den[0] == True)):  # Nhập thành phía vua (kingside)
                            banco_matrix[row][col - 1] = banco_matrix[row][7]  # Xe di chuyển đến cạnh vua
                            banco_matrix[row][7] = '-'
                        elif col < old_col and ((quan_co == 'vt' and xe_trang[1] == True) or (quan_co == 'vd' and xe_den[1] == True)):  # Nhập thành phía hậu (queenside)
                            banco_matrix[row][col + 1] = banco_matrix[row][0]  # Xe di chuyển đến cạnh vua
                            banco_matrix[row][0] = '-'
                if quan_co == 'vt' or quan_co == 'xt':
                    if quan_co == 'xt' and xe_trang[0] == True:
                        xe_trang[0] = False
                    elif quan_co == 'xt' and xe_trang[1] == True:
                        xe_trang[1] = False
                    elif quan_co == 'vt' or (xe_trang == [False,False]):
                        nhapthanh[0] = False
                elif quan_co == 'vd' or quan_co == 'xd':
                    if quan_co == 'xd' and xe_den[0] == True:
                        xe_den[0] = False
                    elif quan_co == 'xd' and xe_den[1] == True:
                        xe_den[1] = False
                    elif quan_co == 'vd' or (xe_den == [False,False]):
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
        for i in range(1,8):
            x.append((row+i,col))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1,8):
            x.append((row-i,col))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1,8):
            x.append((row,col+i))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1,8):
            x.append((row,col-i))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        for z in nuoc_di_hop_le_cua_quan_xe:
            for (i,j) in z:
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
        for i in range(1,8):
            x.append((row+i,col))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1,8):
            x.append((row-i,col))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1,8):
            x.append((row,col+i))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        x = []
        for i in range(1,8):
            x.append((row,col-i))
        nuoc_di_hop_le_cua_quan_xe.append(x)
        for z in nuoc_di_hop_le_cua_quan_xe:
            for (i,j) in z:
                if 0 <= i <= 7 and 0 <= j <= 7:
                    if banco_matrix[i][j] == '-':  
                        nuoc_di_hop_le.append((i, j))
                    elif banco_matrix[i][j][1] == 't':
                        nuoc_di_hop_le.append((i, j))
                        break
                    elif banco_matrix[i][j][1] == 'd':
                        break
    elif quan_co == 'Tt':
        moves = [(-1,-1),(1,1),(-1,1),(1,-1)]
        for i,j in moves:
            new_row = row
            new_col = col
            for k in range(1,8):
                new_row = new_row + i
                new_col = new_col + j 
                if 0 <= new_row  <= 7 and  0 <= new_col <= 7:
                    if banco_matrix[new_row][new_col] == '-':  
                        nuoc_di_hop_le.append((new_row, new_col))
                    elif banco_matrix[new_row][new_col][1] == 'd':
                        nuoc_di_hop_le.append((new_row, new_col))
                        break
                    elif banco_matrix[new_row][new_col][1] == 't':
                        break
    elif quan_co == 'Td':
        moves = [(-1,-1),(1,1),(-1,1),(1,-1)]
        for i,j in moves:
            new_row = row
            new_col = col
            for k in range(1,8):
                new_row = new_row + i
                new_col = new_col + j 
                if 0 <= new_row  <= 7 and  0 <= new_col <= 7:
                    if banco_matrix[new_row][new_col] == '-':  
                        nuoc_di_hop_le.append((new_row, new_col))
                    elif banco_matrix[new_row][new_col][1] == 't':
                        nuoc_di_hop_le.append((new_row, new_col))
                        break
                    elif banco_matrix[new_row][new_col][1] == 'd':
                        break
    elif quan_co == 'ht':
        moves = [(-1,-1),(1,1),(-1,1),(1,-1),(-1,0),(1,0),(0,1),(0,-1)]
        for i,j in moves:
            new_row = row
            new_col = col
            for k in range(1,8):
                new_row = new_row + i
                new_col = new_col + j 
                if 0 <= new_row  <= 7 and  0 <= new_col <= 7:
                    if banco_matrix[new_row][new_col] == '-':  
                        nuoc_di_hop_le.append((new_row, new_col))
                    elif banco_matrix[new_row][new_col][1] == 'd':
                        nuoc_di_hop_le.append((new_row, new_col))
                        break
                    elif banco_matrix[new_row][new_col][1] == 't':
                        break
    elif quan_co == 'hd':
        moves = [(-1,-1),(1,1),(-1,1),(1,-1),(-1,0),(1,0),(0,1),(0,-1)]
        for i,j in moves:
            new_row = row
            new_col = col
            for k in range(1,8):
                new_row = new_row + i
                new_col = new_col + j 
                if 0 <= new_row  <= 7 and  0 <= new_col <= 7:
                    if banco_matrix[new_row][new_col] == '-':  
                        nuoc_di_hop_le.append((new_row, new_col))
                    elif banco_matrix[new_row][new_col][1] == 't':
                        nuoc_di_hop_le.append((new_row, new_col))
                        break
                    elif banco_matrix[new_row][new_col][1] == 'd':
                        break
    elif quan_co == 'vt':
        moves = [(-1,-1),(1,1),(-1,1),(1,-1),(-1,0),(1,0),(0,1),(0,-1)]
        for (i,j) in moves:
            new_row = row + i
            new_col = col + j
            if 0 <= new_row  <= 7 and  0 <= new_col <= 7:
                if banco_matrix[new_row][new_col] == '-':  
                    nuoc_di_hop_le.append((new_row, new_col))
                elif banco_matrix[new_row][new_col][1] == 'd':
                    nuoc_di_hop_le.append((new_row, new_col))
                    continue
                elif banco_matrix[new_row][new_col][1] == 't':
                    continue
    elif quan_co =='vd':
        moves = [(-1,-1),(1,1),(-1,1),(1,-1),(-1,0),(1,0),(0,1),(0,-1)]
        for (i,j) in moves:
            new_row = row + i
            new_col = col + j
            if 0 <= new_row  <= 7 and  0 <= new_col <= 7:
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
                not KiemTraChieu(banco_matrix, 7, 5, 't') and not KiemTraChieu(banco_matrix, 7, 6, 't') and nhapthanh[0]):
            nuoc_di_hop_le.append((7, 6))  # Nhập thành phía vua
        # Nhập thành phía hậu (queenside)
        if (banco_matrix[7][1] == '-' and banco_matrix[7][2] == '-' and banco_matrix[7][3] == '-' and
                banco_matrix[7][0] == 'xt' and not KiemTraChieu(banco_matrix, 7, 4, 't') and
                not KiemTraChieu(banco_matrix, 7, 3, 't') and not KiemTraChieu(banco_matrix, 7, 2, 't') and nhapthanh[0]):
            nuoc_di_hop_le.append((7, 2))  # Nhập thành phía hậu
    elif quan_co == 'vd':  # Vua đen
        # Nhập thành phía vua (kingside)
        if (banco_matrix[0][5] == '-' and banco_matrix[0][6] == '-' and
                banco_matrix[0][7] == 'xd' and not KiemTraChieu(banco_matrix, 0, 4, 'd') and
                not KiemTraChieu(banco_matrix, 0, 5, 'd') and not KiemTraChieu(banco_matrix, 0, 6, 'd') and nhapthanh[1]):
            nuoc_di_hop_le.append((0, 6))  # Nhập thành phía vua
        # Nhập thành phía hậu (queenside)
        if (banco_matrix[0][1] == '-' and banco_matrix[0][2] == '-' and banco_matrix[0][3] == '-' and
                banco_matrix[0][0] == 'xd' and not KiemTraChieu(banco_matrix, 0, 4, 'd') and
                not KiemTraChieu(banco_matrix, 0, 3, 'd') and not KiemTraChieu(banco_matrix, 0, 2, 'd') and nhapthanh[1]):
            nuoc_di_hop_le.append((0, 2))  # Nhập thành phía hậu
    return nuoc_di_hop_le
nhapthanh = [True,True]
xe_trang = [True, True]
xe_den = [True, True]
def KiemTraChieu(banco_matrix, vua_row, vua_col, mau_quan):
    """
    Kiểm tra xem vua có đang bị chiếu hay không.
    - banco_matrix: Ma trận bàn cờ.
    - vua_row, vua_col: Vị trí của vua trên bàn cờ.
    - mau_quan: Màu của quân vua ('t' cho trắng, 'd' cho đen).
    """
    # Kiểm tra các hướng tấn công từ quân đối phương
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = vua_row + dr, vua_col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            quan = banco_matrix[r][c]
            if quan != '-':
                if quan[1] != mau_quan:  # Quân đối phương
                    if (dr, dc) in directions and quan[0] in ['h', 'T']:  # Hậu hoặc tượng
                        return True
                    if (dr == 0 or dc == 0) and quan[0] == 'x':  # Xe
                        return True
                    if abs(dr) == 1 and abs(dc) == 1 and quan[0] == 't' and quan[1] != mau_quan:  # Tốt
                        return True
                break  # Dừng kiểm tra nếu gặp quân đồng minh hoặc quân đối phương
            r += dr
            c += dc

    # Kiểm tra mã (knight)
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in knight_moves:
        r, c = vua_row + dr, vua_col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            quan = banco_matrix[r][c]
            if quan != '-' and quan[0] == 'n' and quan[1] != mau_quan:  # Mã đối phương
                return True

    return False


def KiemTraChieuBi(banco_matrix, vua_row, vua_col, mau_quan):
    """
    Kiểm tra xem vua có đang bị chiếu bí hay không.
    - banco_matrix: Ma trận bàn cờ.
    - vua_row, vua_col: Vị trí của vua trên bàn cờ.
    - mau_quan: Màu của quân vua ('t' cho trắng, 'd' cho đen).
    """
    # Kiểm tra xem vua có đang bị chiếu hay không
    if not KiemTraChieu(banco_matrix, vua_row, vua_col, mau_quan):
        return False

    # Kiểm tra xem có nước đi nào để thoát khỏi chiếu hay không
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = vua_row + dr, vua_col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Di chuyển vua tạm thời
                quan_tam = banco_matrix[new_row][new_col]
                banco_matrix[new_row][new_col] = 'v' + mau_quan
                banco_matrix[vua_row][vua_col] = '-'

                # Kiểm tra xem vua có còn bị chiếu sau khi di chuyển hay không
                if not KiemTraChieu(banco_matrix, new_row, new_col, mau_quan):
                    # Khôi phục lại bàn cờ
                    banco_matrix[vua_row][vua_col] = 'v' + mau_quan
                    banco_matrix[new_row][new_col] = quan_tam
                    return False

                # Khôi phục lại bàn cờ
                banco_matrix[vua_row][vua_col] = 'v' + mau_quan
                banco_matrix[new_row][new_col] = quan_tam

    return True


def KiemTraThangThua(banco_matrix, luot_choi):
    """
    Kiểm tra xem trò chơi đã kết thúc hay chưa (chiếu bí hoặc hòa).
    - banco_matrix: Ma trận bàn cờ.
    - luot_choi: Lượt chơi hiện tại ('t' cho trắng, 'd' cho đen).
    """
    # Tìm vị trí của vua
    vua_row, vua_col = -1, -1
    for row in range(8):
        for col in range(8):
            if banco_matrix[row][col] == 'v' + luot_choi:
                vua_row, vua_col = row, col
                break
        if vua_row != -1:
            break

    if vua_row == -1 or vua_col == -1:
        return "Hòa"  # Không tìm thấy vua (trường hợp bất thường)

    # Kiểm tra chiếu bí
    if KiemTraChieuBi(banco_matrix, vua_row, vua_col, luot_choi):
        return "Chiếu bí! " + ("Trắng" if luot_choi == 't' else "Đen") + " thua."

    # Kiểm tra hòa (không có nước đi hợp lệ)
    for row in range(8):
        for col in range(8):
            if banco_matrix[row][col] != '-' and banco_matrix[row][col][1] == luot_choi:
                nuoc_di_hop_le = TimNuocDi(banco_matrix, row, col)
                if nuoc_di_hop_le:
                    return None  # Trò chơi tiếp tục

    return "Hòa"  # Không có nước đi hợp lệ
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