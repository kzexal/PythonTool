@echo off
rem Chuyển thư mục làm việc về vị trí chứa file script
cd /d "%~dp0"

rem Chạy script Python ẩn cửa sổ console (nếu dùng pythonw) hoặc dùng python tiêu chuẩn
python organize_downloads.py