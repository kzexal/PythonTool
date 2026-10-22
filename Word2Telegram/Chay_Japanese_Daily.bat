@echo off
setlocal
chcp 65001 >nul
title Japanese Daily Vocabulary

REM Chuyen den thu muc chua file BAT va chuong trinh Python
cd /d "%~dp0"

echo ==========================================
echo   JAPANESE DAILY VOCABULARY - TELEGRAM
echo ==========================================
echo.

REM Kiem tra Python
where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON=py"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set "PYTHON=python"
    ) else (
        echo [LOI] Khong tim thay Python.
        echo Hay cai Python va chon "Add Python to PATH", sau do thu lai.
        pause
        exit /b 1
    )
)

REM Kiem tra cac file can thiet
if not exist "japanese_daily.py" (
    echo [LOI] Khong tim thay japanese_daily.py trong thu muc nay.
    pause
    exit /b 1
)

if not exist "config.json" (
    echo [LOI] Khong tim thay config.json trong thu muc nay.
    pause
    exit /b 1
)

if not exist "vocabulary.xlsx" (
    echo [CANH BAO] Khong tim thay vocabulary.xlsx.
    echo Neu file Excel co ten khac, hay sua excel_file trong config.json.
    pause
    exit /b 1
)

REM Cai openpyxl neu chua co
%PYTHON% -c "import openpyxl" >nul 2>nul
if errorlevel 1 (
    echo Dang cai thu vien openpyxl...
    %PYTHON% -m pip install openpyxl
    if errorlevel 1 (
        echo [LOI] Khong cai duoc openpyxl.
        pause
        exit /b 1
    )
)

echo Dang chay chuong trinh...
echo.
%PYTHON% "japanese_daily.py"

if errorlevel 1 (
    echo.
    echo [LOI] Chuong trinh ket thuc voi loi.
    echo Hay kiem tra thong bao ben tren va file japanese_daily.log.
) else (
    echo.
    echo Da chay xong. Hay kiem tra Telegram de xem tin nhan.
)

echo.

endlocal
