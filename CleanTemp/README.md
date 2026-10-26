# CleanTemp — Dọn file tạm trên Windows

Tiện ích Python dọn các file cũ trong thư mục Temp của người dùng. Mặc định, chương trình xét các file có thời gian chỉnh sửa cuối cùng cũ hơn **3 ngày**, bỏ qua file không thể truy cập hoặc đang được chương trình khác sử dụng, và ghi log vào `clean_temp.log`.

## Tính năng

- Tự xác định thư mục Temp thông qua `tempfile.gettempdir()`.
- Cho phép chỉ định số ngày bằng tham số `--days`.
- Có chế độ xem trước `--dry-run`, không xóa file.
- Ghi log với dung lượng luân phiên để hạn chế log tăng vô hạn.
- Bỏ qua symbolic link và xử lý lỗi truy cập file theo cách an toàn hơn.

## Các file chính

| File | Vai trò |
|---|---|
| `clean_temp.py` | Logic dọn file tạm và xử lý tham số dòng lệnh |
| `Clean.bat` | File batch để chạy tiện ích trên Windows |
| `clean_temp.log` | Log hoạt động; được tạo/cập nhật khi chạy |

## Yêu cầu

- Windows và Python 3.
- Không cần cài thư viện bên ngoài; script sử dụng thư viện chuẩn của Python.

## Cách chạy

Mở PowerShell hoặc Command Prompt trong thư mục này:

```powershell
py clean_temp.py --dry-run
```

Nếu danh sách dự kiến xóa hợp lý, chạy thật:

```powershell
py clean_temp.py
```

Đổi ngưỡng tuổi file, ví dụ 7 ngày:

```powershell
py clean_temp.py --days 7
```

Kết hợp tham số để xem trước các file cũ hơn 7 ngày:

```powershell
py clean_temp.py --days 7 --dry-run
```

Có thể chạy `Clean.bat` bằng cách nhấp đúp hoặc gọi từ terminal.

## Kết quả

Chương trình ghi số file đã xử lý, số file bị bỏ qua và dung lượng tương ứng vào log. Ở chế độ xem trước, các file chỉ được liệt kê, không bị xóa.

## Lưu ý an toàn

- **Luôn chạy `--dry-run` trước lần chạy đầu tiên.**
- Chương trình có thể xóa vĩnh viễn các file cũ trong thư mục Temp; không dùng nó để dọn thư mục dữ liệu cá nhân.
- Một số ứng dụng có thể cần file tạm lâu hơn dự kiến. Tự cân nhắc ngưỡng `--days`.
- Log có thể chứa đường dẫn hệ thống của máy tính.
