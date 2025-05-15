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
### So sánh thuật toán:
1. Đối với thuật toán DFS: Được hoạt động theo quy luật LIFO (Last In First Out), khi đường đi của một quân cờ vào cuối thì sẽ được đi trước. Trong trường hợp AI ở phía quân đen thì nước đi cuối cùng là của quân tốt bên phải, vì thế AI sẽ đi quân tốt đó đến khi không đi được nữa thì chuyển sang quân tiếp theo
2. Đối với thuật toán And-Or Search: Thì node Or sẽ đưa ra các đường đi khả dỉ cho AI và cho nó một trọng số mỗi nước đi dựa trên tính toán của hàm evaluate_board và được sắp xếp theo thứ tự từ nước đi tốt nhất đến tệ nhất, node And được sử dụng để liệt kê ra các nước đi có thể có của đối thủ sau khi thực hiện một hành động bất kì tại node Or. Nước đi của AI sẽ được chọn ngẫu nhiên dựa vào trong số tại node Or, trọng số càng cao tỉ lệ được chọn càng cao. Vì thế sẽ có một số nước đi là tối ưu và một số nước đi là ngu ngốc
3. Đối với thuật toán Backtracking: dùng đệ quy để xét hết nước đi có thể đi được và lấy nước đi tối ưu điều kiện để dừng là duyệt hết độ sâu hoặc là tìm được trạng thái mà vua bên phe đối thủ bị chiếu bên cạnh đó trong lúc duyệt các nước đi có thể đi được thì cũng xét các ràng buộc để giảm bớt các nước đi "ngu" (khiến vua bị chiếu) hàm trả về giá trị của nước đi và nước đi

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
### So sánh thuật toán:
1. Đối với A*: Thì nhóm sử dụng Heuristic là khoảng cách Manhattan, vì Heuristic làm cũng khá là tối ưu, vì thế quảng đường tìm ra là khá tốt.
2. Đối với Steepest Hill Climbing: Thì nó sẽ chọn đường đi dóc nhất, khi gặp vị trí mà khoảng cách Manhattan lớn hơn hiện tại thì sẽ kẹt ở cục bộ
3. Đối với q-learning thì nó sẽ chạy theo bảng q-table và kiểm thử đúng sai nhận được điểm khác nhau và nhận điểm thưởng khác nhau. Ví dụ: Đi vào tường thì -100, đi vào đường chưa đi -1, đi vào đường đã đi -2, tới đích +100 và dừng lại khi đã tới đích
## Link Github
Để biết thêm chi tiết và mã nguồn của dự án, bạn có thể truy cập:
[https://github.com/plat16022005/do-an-AI](https://github.com/plat16022005/do-an-AI)
