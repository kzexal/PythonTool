# PythonTool

Bộ công cụ Python cá nhân dành cho tự động hóa các tác vụ học tập và sử dụng máy tính trên Windows. Repository hiện gồm các tiện ích độc lập: chuyển Markdown thành PowerPoint theo template HUST, tạo flashcard tiếng Nhật cho Anki từ Excel, gửi từ vựng hằng ngày qua Telegram, dọn file tạm và sắp xếp thư mục Downloads.

## 📚 Danh mục công cụ

| Thư mục | Chức năng | Tài liệu |
|---|---|---|
| `Slide/` | Chuyển nội dung Markdown thành PowerPoint theo template HUST | [Slide/README.md](Slide/README.md) |
| `JapaneseFlashcards/` | Kiểm tra dữ liệu từ vựng Excel, tạo bộ thẻ Anki `.apkg`, theo dõi thay đổi và hỗ trợ đồng bộ Anki | [JapaneseFlashcards/README.md](JapaneseFlashcards/README.md) |
| `Word2Telegram/` | Gửi từ vựng tiếng Nhật qua Telegram theo lịch chạy được cấu hình bên ngoài | [Word2Telegram/README.md](Word2Telegram/README.md) |
| `CleanTemp/` | Dọn các file cũ trong thư mục Temp của Windows | [CleanTemp/README.md](CleanTemp/README.md) |
| `OrganizeDownloads/` | Phân loại file trong Downloads theo phần mở rộng | [OrganizeDownloads/README.md](OrganizeDownloads/README.md) |

Mỗi công cụ hoạt động độc lập; bạn chỉ cần cài thư viện và chạy script trong thư mục tương ứng.

## 🧰 Yêu cầu chung

- Windows được khuyến nghị vì một số script sử dụng thư mục và lệnh dành cho Windows.
- Python 3 và `pip`.
- Các thư viện riêng của từng công cụ được liệt kê trong README hoặc file `requirements.txt` tương ứng.
- Với công cụ sử dụng Telegram, cần có bot Telegram và cấu hình thông tin bot/chat theo hướng dẫn riêng.
- Với tính năng đồng bộ trực tiếp Anki, cần cài Anki và add-on AnkiConnect.

## 🚀 Bắt đầu nhanh

### 1. Tải repository

```powershell
git clone https://github.com/kzexal/PythonTool.git
cd PythonTool
```

Hoặc tải repository dưới dạng ZIP từ GitHub và giải nén.

### 2. Chọn công cụ cần dùng

Đi tới thư mục của công cụ. Ví dụ tạo flashcard tiếng Nhật:

```powershell
cd JapaneseFlashcards
py -m pip install -r requirements.txt
py main.py
```

Hãy đọc README của thư mục đó trước khi chạy để chuẩn bị file đầu vào và cấu hình cần thiết. Không phải công cụ nào cũng cần thư viện bên ngoài.

## 🗂️ Cấu trúc repository

```text
PythonTool/
├── README.md
├── Slide/
│   ├── README.md
│   ├── md2pptx.py
│   ├── input.md
│   └── Runmd2pptx.bat
├── JapaneseFlashcards/
│   ├── README.md
│   ├── main.py
│   ├── gui.py
│   ├── watch_excel.py
│   ├── sync_anki.py
│   ├── requirements.txt
│   ├── input/
│   └── output/
├── Word2Telegram/
│   └── README.md
├── CleanTemp/
│   ├── README.md
│   ├── clean_temp.py
│   └── Clean.bat
└── OrganizeDownloads/
    ├── README.md
    ├── organize_downloads.py
    └── RunOrganize.bat
```

Cây thư mục trên tập trung vào các file chính; một số file cấu hình, log, dữ liệu đầu vào/đầu ra và file build có thể xuất hiện thêm trong repository.

## 🔐 Cấu hình và an toàn

- Không commit bot token, API key, mật khẩu hoặc thông tin riêng tư vào Git.
- Kiểm tra kỹ đường dẫn và chế độ hoạt động trước khi chạy script có thể xóa hoặc di chuyển file.
- Với công cụ dọn Temp và sắp xếp Downloads, nên chạy chế độ xem trước nếu có hỗ trợ và kiểm tra kết quả trước khi thao tác thật.
- File log có thể chứa đường dẫn máy tính hoặc thông tin vận hành; hãy kiểm tra trước khi chia sẻ công khai.
- Sao lưu dữ liệu quan trọng trước khi chạy các công cụ thao tác trên file.

## 🛠️ Khắc phục sự cố

- **Không nhận diện lệnh `py` hoặc `python`:** cài Python và bật tùy chọn thêm Python vào PATH, sau đó mở lại terminal.
- **Thiếu thư viện:** chạy lệnh cài đặt trong README của công cụ đang dùng.
- **Không tìm thấy file đầu vào:** kiểm tra tên file, đường dẫn và vị trí đặt file.
- **Không kết nối được AnkiConnect:** mở Anki và kiểm tra add-on AnkiConnect.
- **Telegram không gửi được tin nhắn:** kiểm tra bot token, chat ID, quyền nhắn tin của bot và kết nối mạng.

## 🤝 Đóng góp và cải tiến

Khi thêm một công cụ mới, nên đặt trong một thư mục riêng và tạo README mô tả mục đích, yêu cầu, cấu hình, cách chạy, file đầu vào/đầu ra và lưu ý an toàn.

## 📄 License

Chưa xác định giấy phép chung cho toàn repository. Nếu muốn người khác sử dụng, chỉnh sửa hoặc phân phối lại dự án, hãy bổ sung file `LICENSE` phù hợp với mong muốn của tác giả.
