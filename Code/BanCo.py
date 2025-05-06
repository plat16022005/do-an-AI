import pygame
import UI
loai = UI.style
# Load và scale các quân cờ trắng
xe_trang = pygame.image.load(f'Sprite/xe_trang({loai}).png')
xe_trang = pygame.transform.scale(xe_trang, (100, 100))

ngua_trang = pygame.image.load(f'Sprite/ngua_trang({loai}).png')
ngua_trang = pygame.transform.scale(ngua_trang, (100, 100))

tuong_trang = pygame.image.load(f'Sprite/tuong_trang({loai}).png')
tuong_trang = pygame.transform.scale(tuong_trang, (100, 100))

hau_trang = pygame.image.load(f'Sprite/hau_trang({loai}).png')
hau_trang = pygame.transform.scale(hau_trang, (100, 100))

vua_trang = pygame.image.load(f'Sprite/vua_trang({loai}).png')
vua_trang = pygame.transform.scale(vua_trang, (100, 100))

tot_trang = pygame.image.load(f'Sprite/tot_trang({loai}).png')
tot_trang = pygame.transform.scale(tot_trang, (100, 100))

# Load và scale các quân cờ đen
xe_den = pygame.image.load(f'Sprite/xe_den({loai}).png')
xe_den = pygame.transform.scale(xe_den, (100, 100))

ngua_den = pygame.image.load(f'Sprite/ngua_den({loai}).png')
ngua_den = pygame.transform.scale(ngua_den, (100, 100))

tuong_den = pygame.image.load(f'Sprite/tuong_den({loai}).png')
tuong_den = pygame.transform.scale(tuong_den, (100, 100))

hau_den = pygame.image.load(f'Sprite/hau_den({loai}).png')
hau_den = pygame.transform.scale(hau_den, (100, 100))

vua_den = pygame.image.load(f'Sprite/vua_den({loai}).png')
vua_den = pygame.transform.scale(vua_den, (100, 100))

tot_den = pygame.image.load(f'Sprite/tot_den({loai}).png')
tot_den = pygame.transform.scale(tot_den, (100, 100))


class Board():
    def __init__(self, screen):
        self.screen = screen
# Vẽ bàn cờ
    def VeBanCo(self, valid_moves=[]):
        print(loai)
        board_colors = {}
        for row in range(8):
            for col in range(8):
                base_color = (211, 211, 211) if (row + col) % 2 == 0 else (165, 42, 42)
                pygame.draw.rect(self.screen, base_color, [col * 100, row * 100, 100, 100])
                board_colors[(row, col)] = base_color

        # Vẽ màu pha trộn cho từng ô đi hợp lệ
        highlight_color = (255, 255, 100)  # Màu vàng nhạt
        for (row, col) in valid_moves:
            base_color = board_colors.get((row, col), (240, 217, 181))  # Lấy màu gốc
            mixed_color = (
                (base_color[0] + highlight_color[0]) // 2, 
                (base_color[1] + highlight_color[1]) // 2, 
                (base_color[2] + highlight_color[2]) // 2
            )  # Pha trộn màu

            pygame.draw.rect(self.screen, mixed_color, [col * 100, row * 100, 100, 100])
# Vẽ quân cờ theo ma trận
    def VeQuanCo(self, matrix):
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                if col == 'xt':
                    xe_trang_rect = xe_trang.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(xe_trang, xe_trang_rect)
                elif col == 'nt':
                    ngua_trang_rect = ngua_trang.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(ngua_trang, ngua_trang_rect)
                elif col == 'Tt':
                    tuong_trang_rect = tuong_trang.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(tuong_trang, tuong_trang_rect)
                elif col == 'tt':
                    tot_trang_rect = tot_trang.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(tot_trang, tot_trang_rect)
                elif col == 'ht':
                    hau_trang_rect = hau_trang.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(hau_trang, hau_trang_rect)
                elif col == 'vt':
                    vua_trang_rect = vua_trang.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(vua_trang, vua_trang_rect)

                elif col == 'xd':
                    xe_den_rect = xe_den.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(xe_den, xe_den_rect)
                elif col == 'nd':
                    ngua_den_rect = ngua_den.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(ngua_den, ngua_den_rect)
                elif col == 'Td':
                    tuong_den_rect = tuong_den.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(tuong_den, tuong_den_rect)
                elif col == 'td':
                    tot_den_rect = tot_den.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(tot_den, tot_den_rect)
                elif col == 'hd':
                    hau_den_rect = hau_den.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(hau_den, hau_den_rect)
                elif col == 'vd':
                    vua_den_rect = vua_den.get_rect(center=(50 + j * 100, 50 + i * 100))
                    self.screen.blit(vua_den, vua_den_rect)