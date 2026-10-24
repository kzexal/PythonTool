# Bộ công cụ xuất Markdown sang Word (Đồ án tốt nghiệp ĐHBKHN)

Bộ công cụ tự động chuyển đổi các chương viết bằng Markdown sang file Word (`.docx`) chuẩn quy cách Đồ án tốt nghiệp Đại học Bách Khoa Hà Nội theo **Mẫu ĐATN 2019 version 1.1**.

---

## 1. Yêu cầu hệ thống
- Windows 10/11
- Python 3.10 trở lên
- Microsoft Word (để cập nhật trường mục lục và số trang tự động)

---

## 2. Cài đặt lần đầu

1. Mở PowerShell tại thư mục dự án:
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

2. Tạo template sạch chuẩn quy cách từ `Mẫu ĐATN_2019_version 1_1.docx`:
```powershell
.\.venv\Scripts\python.exe make_template.py
```
*Lệnh này sẽ tự động sinh file `template_clean.docx` đã có sẵn: Trang bìa, Lời cam đoan, Lời cảm ơn, Tóm tắt nội dung đồ án, Mục lục, Danh mục hình vẽ, Danh mục bảng biểu và cấu hình căn lề chuẩn A4.*

---

## 3. Quy cách viết nội dung (theo Mẫu ĐATN 2019)

| Thành phần | Cú pháp Markdown | Ghi chú quy chuẩn |
| :--- | :--- | :--- |
| **Tiêu đề chương** | `# CHƯƠNG 1. MỞ ĐẦU` | Style `Heading 1`, tự động đánh số chương và ngắt trang mới |
| **Tiêu đề mục** | `## 1.1 Đặt vấn đề` | Style `Heading 2`, cấp 1 |
| **Tiêu đề mục con** | `### 1.1.1 Mục tiêu` | Style `Heading 3`, cấp 2 |
| **Đoạn văn** | Đoạn văn bản thường | Style `Normal`, Times New Roman 13pt, căn đều hai bên |
| **Hình vẽ / Ảnh** | `![Tên hình](../images/so_do.png)` | Chiều rộng **không quá 75%** chiều rộng nội dung (<= 11.25 cm / 4.43 in), căn giữa; chú thích đặt dưới hình |
| **Bảng biểu** | `Table: Tên bảng`<br>`\| Cột 1 \| Cột 2 \|` | Chiều rộng **không quá 75%** nội dung; chú thích đặt trên bảng |
| **Trích dẫn** | `[@esp32]` | Khớp với key trong `references.json`, tự sinh danh mục tài liệu tham khảo |

---

## 4. Xuất file Word

### Cách 1: Nhanh nhất (Click đúp chuột)
Click đúp trực tiếp vào file **`xuat_bao_cao.bat`**.

### Cách 2: Chạy từ dòng lệnh
```powershell
.\.venv\Scripts\python.exe build_report.py
```

File kết quả sẽ là **`Bao_cao_do_an.docx`**.

---

## 5. Cập nhật Mục lục & Số trang trong Microsoft Word
1. Mở `Bao_cao_do_an.docx` bằng Word.
2. Nếu hiện bảng hỏi cập nhật trường ("*This document contains fields that may refer to other files...*"), nhấn **Yes**.
3. Nhấn tổ hợp phím **`Ctrl + A`** để chọn toàn bộ văn bản.
4. Nhấn **`F9`** -> Chọn **Update entire table** (Cập nhật toàn bộ bảng) -> Nhấn **OK**.
Word sẽ tự động đồng bộ:
- Trang Mục lục (TOC)
- Trang Danh mục hình vẽ (TOF Hình)
- Trang Danh mục bảng biểu (TOF Bảng)
- Toàn bộ số trang chính xác 100%.

---

## 6. Các thông số căn lề chuẩn (Mẫu ĐATN 2019)
- **Khổ giấy:** A4 (21.0 cm x 29.7 cm)
- **Lề trên (Top):** 2.0 cm
- **Lề dưới (Bottom):** 2.0 cm
- **Lề trái (Left):** 3.5 cm
- **Lề phải (Right):** 2.5 cm
- **Chiều rộng nội dung:** 15.0 cm (ảnh/bảng tối đa 75% = 11.25 cm)
- **Phông chữ:** Times New Roman, cỡ 13pt
