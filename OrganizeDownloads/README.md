# OrganizeDownloads — Sắp xếp thư mục Downloads

Script `organize_downloads.py` phân loại các file nằm trực tiếp trong thư mục Downloads của người dùng thành các thư mục con dựa trên phần mở rộng của file.

## Nhóm file

| Thư mục đích | Ví dụ phần mở rộng |
|---|---|
| `Tai_lieu` | PDF, DOCX, TXT, PPTX, XLSX, CSV, MD |
| `Hinh_anh` | JPG, PNG, GIF, WEBP, SVG, HEIC |
| `Video` | MP4, MKV, AVI, MOV, WEBM |
| `Am_thanh` | MP3, WAV, FLAC, AAC, M4A |
| `File_nen` | ZIP, RAR, 7Z, TAR, GZ |
| `Cai_dat` | EXE, MSI, APK, DEB, RPM |
| `Ma_nguon` | PY, CS, JAVA, C/C++, JS, TS, HTML, CSS, SQL, JSON |
| `Khac` | Các phần mở rộng chưa được khai báo |

## Các file chính

- `organize_downloads.py`: cấu hình đường dẫn, nhóm phần mở rộng và thực hiện phân loại.
- `RunOrganize.bat`: file batch khởi chạy tiện ích trên Windows.

## Yêu cầu

- Python 3.
- Không cần cài thư viện bên ngoài.

## Cách sử dụng an toàn

1. Mở `organize_downloads.py`.
2. Đặt `DRY_RUN = True` để xem trước các thao tác dự kiến.
3. Chạy:

   ```powershell
   py organize_downloads.py
   ```

4. Kiểm tra các dòng `[XEM TRUOC]`.
5. Khi đã chắc chắn, đổi thành `DRY_RUN = False` rồi chạy lại để di chuyển file thật.

Có thể chạy bằng `RunOrganize.bat` nếu file này nằm trong thư mục.

## Cách xử lý trùng tên

Nếu thư mục đích đã có file cùng tên, script tự chọn tên mới như `document_1.pdf`, `document_2.pdf` để tránh ghi đè.

## Lưu ý

- Script chỉ quét các file nằm trực tiếp trong Downloads, không quét đệ quy các thư mục con.
- Các file được **di chuyển**, không phải sao chép. Hãy dùng chế độ xem trước trước khi chạy thật.
- Đường dẫn Downloads được xác định từ thư mục home của tài khoản đang chạy chương trình.
- Có thể mở rộng các nhóm file bằng cách chỉnh dictionary `FILE_TYPES` trong script.
