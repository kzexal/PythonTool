# Markdown to PPTX (HUST Template)

Dự án này cung cấp một công cụ (Python script) giúp chuyển đổi nhanh chóng nội dung từ file Markdown (`.md`) sang định dạng bài thuyết trình PowerPoint (`.pptx`) sử dụng template chuẩn của Đại học Bách Khoa Hà Nội (HUST).

## 🌟 Tính năng nổi bật

* **Tự động hóa**: Biến file text đơn giản thành bài thuyết trình hoàn chỉnh chỉ với một dòng lệnh.

* **Tuân thủ chuẩn HUST**: Tự động sử dụng màu sắc, phông chữ (Arial), và bố cục từ template của Đại học Bách Khoa Hà Nội.

* **Tự động tạo cấu trúc**: Hỗ trợ tạo trang bìa, tự động sinh trang "Nội dung chính" (Mục lục) dựa trên các chương, và các slide ngăn cách chương.

* **Định dạng thông minh**:

  * Tự động điều chỉnh kích thước chữ dựa trên số lượng nội dung trong slide.

  * Hỗ trợ danh sách đa cấp (bullet points cấp 1 và 2).

  * Tự động đánh số trang (bỏ qua trang bìa và trang kết thúc).

## ⚙️ Yêu cầu hệ thống

Để chạy được dự án này, máy tính của bạn cần có Python và thư viện hỗ trợ. 

1. **Cài đặt Python**: Bạn có thể cài đặt cực nhanh thông qua dòng lệnh (Terminal / Command Prompt) tùy theo hệ điều hành:
   * **Windows** (Mở cmd hoặc PowerShell):
     ```
     winget install Python.Python.3
     ```
     *(Sau khi cài xong, hãy tắt và mở lại Terminal để máy nhận diện lệnh. Hoặc bạn có thể tải bộ cài thủ công tại [python.org](https://www.python.org/downloads/) - nhớ tích **"Add python.exe to PATH"**).*
   * **macOS** (Yêu cầu có Homebrew):
     ```
     brew install python
     ```
   * **Linux (Ubuntu/Debian)**:
     ```
     sudo apt update && sudo apt install python3 python3-pip
     ```

2. **Cài đặt thư viện `python-pptx`**: Sau khi đã có Python, mở terminal và chạy lệnh:

   ```
   pip install python-pptx
   
   ```

## 🚀 Hướng dẫn chạy nhanh

Để chạy chương trình một cách đơn giản nhất, hãy đảm bảo bạn có file `input.md` và file template `HUST_PPT_template_2022_Blue_16x9.pptx` trong cùng thư mục.

Sau đó, mở terminal/cmd và gõ lệnh sau:

```
py md2pptx.py

```

*(Nếu hệ điều hành của bạn không nhận lệnh `py`, hãy thử dùng `python md2pptx.py` hoặc `python3 md2pptx.py`)*

*Chương trình sẽ tự động đọc file `input.md` và tạo ra file kết quả `output.pptx`.*

## 📝 Quy ước viết file Markdown

Để script có thể hiểu và chuyển đổi chính xác, file `.md` của bạn cần tuân theo quy ước sau:

| Ký hiệu | Ý nghĩa | Kết quả trên slide | 
| ----- | ----- | ----- | 
| `## Tên` | **Tên chương** | Slide ngăn cách, nền xanh đậm, chữ trắng to | 
| `# Tên` | **Tiêu đề slide** | Thanh tiêu đề của slide nội dung | 
| `- text` | **Nội dung bullet cấp 1** | • trong thân slide | 
| `  - text` (2 dấu cách) | **Bullet cấp 2** | ◦ thụt vào | 

*(Mẹo: Bạn có thể sử dụng cú pháp `[Tên hiển thị](link)` để chèn đường dẫn - hyperlink vào trong các bullet)*

### Ví dụ mẫu (`input.md`)

```
## Phần 1: Giới thiệu chung

# Tổng quan về Trí tuệ Nhân tạo
- Đây là một slide ít chữ (chỉ có 2 dòng)
- Bạn sẽ thấy cỡ chữ của slide này tự động to ra.

# Các nguồn tài liệu tham khảo
- Bạn có thể vào xem trang chủ của [Đại học Bách Khoa](https://hust.edu.vn).
  - Đây là bullet cấp 2 thụt lề

```
