# Hướng dẫn sử dụng ứng dụng Cờ Vua AI và Giải Mê Cung

Dự án bao gồm hai ứng dụng chính: một trò chơi Cờ Vua với các đối thủ AI và một ứng dụng tạo và giải Mê Cung.

## 1. Ứng dụng Cờ Vua AI

Ứng dụng cho phép bạn chơi cờ vua với các chế độ khác nhau, bao gồm chơi với người khác, chơi với máy (AI) hoặc xem hai AI đấu với nhau.

### Yêu cầu hệ thống:
* Python
* Pygame
* Thư mục `Sprite` chứa hình ảnh các quân cờ phải nằm cùng cấp với file thực thi.

### Hướng dẫn thực thi:
1.  Mở terminal (hoặc command prompt).
2.  Di chuyển đến thư mục `Code` của dự án.
3.  Chạy lệnh: `python main.py`.
4.  Trên giao diện ứng dụng:
    * Nhấn nút "Start".
    * Chọn chế độ chơi mong muốn (P vs P, P vs AI, AI vs AI).
    * Nếu chọn chế độ chơi với AI (P vs AI hoặc AI vs AI), hãy chọn thuật toán AI bạn muốn sử dụng.
5.  Trò chơi sẽ kết thúc khi một bên thắng, hoặc khi ván cờ hòa (hòa cờ, chiếu bí).

## 2. Ứng dụng Tìm Đường Đi Trong Mê Cung

Ứng dụng này cho phép bạn tạo ra các mê cung ngẫu nhiên bằng nhiều thuật toán khác nhau và sau đó tìm đường đi từ điểm bắt đầu đến điểm kết thúc.

### Yêu cầu hệ thống:
* Python
* Pygame
* NumPy
* File ảnh nền `background.jpg` phải nằm trong thư mục `UI.py` (Lưu ý: theo tài liệu gốc, có vẻ tên thư mục này là `UI.py`, bạn có thể cần kiểm tra lại cấu trúc thư mục thực tế của dự án).

### Hướng dẫn thực thi:
1.  Mở terminal (hoặc command prompt).
2.  Di chuyển đến thư mục `find-way` của dự án.
3.  Chạy lệnh: `python Main.py`.
4.  Trên giao diện ứng dụng:
    * Nhấn nút "Start".
    * Chọn kích thước cho mê cung.
    * Chọn thuật toán để tạo mê cung.
    * Nhấn nút "điểm đích ngẫu nhiên" để chương trình tự chọn điểm kết thúc.
    * Sau khi đã có điểm đích, chọn thuật toán để tìm đường đi trong mê cung.
5.  Ứng dụng Pygame sẽ thoát khi người dùng đóng cửa sổ.

## Link Github
Để biết thêm chi tiết và mã nguồn của dự án, bạn có thể truy cập:
[https://github.com/plat16022005/do-an-AI](https://github.com/plat16022005/do-an-AI)