# Word2Telegram — Từ vựng tiếng Nhật qua Telegram

Công cụ đọc danh sách từ vựng từ Excel và gửi một nhóm từ mỗi lần chạy qua Telegram Bot API. Script được thiết kế để có thể gọi theo lịch bằng Task Scheduler hoặc một dịch vụ chạy định kỳ; bản thân script không tự tạo lịch chạy.

## Tính năng

- Đọc lại file Excel ở mỗi lần chạy để lấy dữ liệu mới nhất đã lưu.
- Gửi mặc định 5 từ mỗi lần chạy.
- Có thể gửi theo thứ tự trong file hoặc bật chọn ngẫu nhiên bằng cách chỉnh `RANDOM_ORDER`.
- Hỗ trợ từ, cách đọc, nghĩa tiếng Việt, câu ví dụ và bản dịch ví dụ.
- Lưu trạng thái các từ đã gửi trong `state.json` để tránh lặp lại trước khi hết một vòng.
- Ghi thông tin vận hành và lỗi vào `japanese_daily.log`.

## Các file chính

| File | Vai trò |
|---|---|
| `japanese_daily.py` | Đọc Excel, chọn từ, tạo tin nhắn và gửi Telegram |
| `config.json` | Cấu hình bot, chat và tùy chọn file Excel |
| `state.json` | Trạng thái các từ đã gửi |
| `Chay_Japanese_Daily.bat` | File batch chạy script trên Windows |
| `japanese_daily.log` | Log chạy chương trình |

Không chia sẻ công khai `config.json` nếu file có chứa bot token hoặc thông tin riêng tư.

## Yêu cầu

- Python 3.
- Thư viện `openpyxl`:

  ```powershell
  py -m pip install openpyxl
  ```

- Một Telegram bot và chat ID đích.
- File Excel có các cột bắt buộc `Japanese`, `Reading`, `Vietnamese`; các cột `Example` và `ExampleMeaning` là tùy chọn.

## Cấu hình

Tạo hoặc kiểm tra `config.json` trong thư mục này. Script đọc các khóa `bot_token` và `chat_id`; có thể chỉ định thêm `excel_file` và `sheet_name`. Nếu `excel_file` là đường dẫn tương đối, đường dẫn được tính từ thư mục `Word2Telegram`. Nếu bỏ qua, script dùng `vocabulary.xlsx` trong thư mục đó.

Ví dụ cấu trúc (thay các giá trị mẫu bằng thông tin thật của bạn):

```json
{
  "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
  "chat_id": "YOUR_CHAT_ID",
  "excel_file": "vocabulary.xlsx",
  "sheet_name": "Vocabulary"
}
```

Đặt file Excel tại đúng đường dẫn cấu hình. Nếu bỏ qua `sheet_name`, script dùng sheet đang hoạt động đầu tiên.

## Chạy thủ công

Từ thư mục này:

```powershell
py -m pip install openpyxl
py japanese_daily.py
```

Hoặc chạy `Chay_Japanese_Daily.bat`.

## Tự động gửi mỗi ngày

Dùng Windows Task Scheduler khi máy tính thường bật vào giờ gửi. Nếu muốn gửi ngay cả khi laptop tắt, cần triển khai script lên một máy chủ hoặc dịch vụ cloud có khả năng chạy định kỳ; Task Scheduler trên laptop không thể chạy khi máy đã tắt.

Khi triển khai lên cloud, đưa token vào biến môi trường hoặc kho bí mật của nền tảng nếu có, không đưa token thật vào Git.

## Lưu ý

- Excel cần được lưu trước thời điểm script chạy.
- Trạng thái `state.json` được ghi sau khi gửi thành công.
- Kiểm tra log nếu tin nhắn không được gửi.
- Không commit bot token, chat ID riêng tư hoặc dữ liệu từ vựng cá nhân nếu bạn không muốn công khai chúng.
