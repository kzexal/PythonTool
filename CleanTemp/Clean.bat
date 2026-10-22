@echo off
:: Chuyển thư mục làm việc về cùng thư mục với file bat
cd /d "%~dp0"

echo Dang chay clean_temp.py de don dep cac file tam cu...
:: Chạy file Python (mặc định xóa file cũ hơn 3 ngày)
python clean_temp.py

echo.
echo Hoan thanh!
:: Đợi 2 giây để hiển thị chữ "Hoan thanh!" rồi tự tắt
timeout /t 2 >nul