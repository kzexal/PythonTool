# JapaneseFlashcards — Tạo flashcard tiếng Nhật cho Anki

JapaneseFlashcards chuyển dữ liệu từ vựng trong Excel thành bộ thẻ Anki `.apkg`. Công cụ hỗ trợ kiểm tra dữ liệu, phát hiện bản ghi trùng, tạo báo cáo, giao diện Windows và tự tạo lại bộ thẻ khi file Excel thay đổi.

## Tính năng

- Đọc từ vựng từ sheet `Vocabulary` trong file Excel.
- Kiểm tra các cột bắt buộc và phát hiện dữ liệu thiếu hoặc trùng.
- Chuẩn hóa Unicode và khoảng trắng trước khi so sánh.
- Tạo note/flashcard với ID ổn định để giảm nguy cơ tạo bản ghi mới ngoài ý muốn khi xuất lại.
- Ghi báo cáo kiểm tra vào `output/import_report.txt`.
- Xuất file `output/Japanese_Vocabulary.apkg` bằng cách tạo file tạm trước khi thay thế file đích.
- Cung cấp GUI qua `gui.py` và trình theo dõi Excel qua `watch_excel.py`.
- Có các script bổ trợ cho cập nhật workbook và đồng bộ với Anki.

## Cấu trúc

| File/thư mục | Vai trò |
|---|---|
| `main.py` | Quy trình chính: đọc Excel, kiểm tra, tạo note/deck, xuất APKG và báo cáo |
| `gui.py` | Giao diện Tkinter để chọn Excel, chạy tạo APKG và theo dõi trạng thái |
| `watch_excel.py` | Theo dõi file Excel mặc định và chạy lại quá trình tạo APKG khi có thay đổi |
| `sync_anki.py` | Đồng bộ dữ liệu Excel với Anki thông qua AnkiConnect |
| `sync_anki_backup.py` | Bản script đồng bộ dự phòng |
| `upgrade_workbook.py` | Tiện ích nâng cấp/cập nhật cấu trúc workbook |
| `input/` | File Excel nguồn và dữ liệu đầu vào |
| `output/` | APKG, báo cáo nhập liệu và log đồng bộ |
| `requirements.txt` | Các thư viện Python cần cài |
| `run_update.bat` | File batch hỗ trợ chạy quy trình cập nhật |
| `JapaneseFlashcards.spec`, `build/` | Cấu hình và đầu ra liên quan đến đóng gói ứng dụng |

## Yêu cầu

- Python 3 trên Windows được khuyến nghị.
- File Excel nguồn, mặc định là `input/vocabulary.xlsx`.
- Các thư viện trong `requirements.txt`: `watchdog`, `openpyxl`, `genanki`.

Cài đặt:

```powershell
py -m pip install -r requirements.txt
```

## Định dạng Excel

Mặc định, file `input/vocabulary.xlsx` phải có sheet tên `Vocabulary`.

Các cột bắt buộc:

- `Japanese`: từ/cụm từ tiếng Nhật.
- `Vietnamese`: nghĩa tiếng Việt.

Các cột tùy chọn được hỗ trợ trong quy trình chính gồm `Reading`, `Example`, `ExampleMeaning`, `JLPT`, `Notes`, `Tags`, `Radicals` và `Mnemonics`. Tên cột được so khớp không phân biệt chữ hoa/chữ thường; thứ tự cột không quan trọng.

## Chạy quy trình chính

Từ thư mục này:

```powershell
py main.py
```

Khi thành công, file đầu ra được ghi tại:

- `output/Japanese_Vocabulary.apkg`
- `output/import_report.txt`

Nếu có dòng dữ liệu thiếu, trùng hoặc cảnh báo, hãy mở báo cáo để xem chi tiết. Nếu không có từ hợp lệ, chương trình không xuất bộ thẻ mới.

## Giao diện và tự động cập nhật

Chạy giao diện:

```powershell
py gui.py
```

Giao diện cho phép chọn file Excel, khởi chạy quy trình tạo APKG và bật/tắt theo dõi file đã chọn.

Hoặc chạy watcher dòng lệnh:

```powershell
py watch_excel.py
```

Watcher mặc định theo dõi `input/vocabulary.xlsx`. Sau khi sửa Excel, hãy lưu file và để watcher chạy; nhấn `Ctrl+C` để dừng. Việc tự động cập nhật chỉ hoạt động khi watcher hoặc GUI đang chạy.

## Đồng bộ trực tiếp với Anki

`sync_anki.py` sử dụng AnkiConnect tại `http://127.0.0.1:8765`. Để dùng chức năng này:

1. Cài và mở Anki.
2. Cài add-on AnkiConnect.
3. Kiểm tra cấu hình đường dẫn dự án trong script đồng bộ, vì script hiện có đường dẫn Windows được ghi trực tiếp.
4. Đảm bảo loại note và các trường trong Anki phù hợp với script.
5. Chạy script đồng bộ và kiểm tra log.

Đây là quy trình riêng với việc xuất APKG; không cần Anki đang mở chỉ để chạy `main.py`.

## Lưu ý

- Sao lưu file Excel và bộ thẻ Anki trước khi thay đổi quy trình đồng bộ.
- Không thay đổi `DECK_ID`, `MODEL_ID` hoặc định danh note một cách tùy tiện nếu muốn giữ tính ổn định qua các lần xuất.
- Các file trong `output/` và `build/` là đầu ra được tạo trong quá trình sử dụng/đóng gói.
- Tránh commit dữ liệu cá nhân hoặc file Excel có nội dung riêng tư.
