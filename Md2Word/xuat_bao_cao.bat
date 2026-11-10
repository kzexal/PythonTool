@echo off
setlocal
cd /d "%~dp0"

py -3.13 build_report.py
if errorlevel 1 (
  echo.
  echo Xuat bao cao that bai. Hay doc thong bao loi o tren.
) else (
  echo.
  echo Da xuat output.docx
)
pause
