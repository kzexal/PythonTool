@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Chua cai dat moi truong Python.
  echo Hay mo PowerShell tai thu muc nay va chay:
  echo py -m venv .venv
  echo .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  pause
  exit /b 1
)
".venv\Scripts\python.exe" build_report.py
if errorlevel 1 (
  echo.
  echo Xuat bao cao that bai. Hay doc thong bao loi o tren.
) else (
  echo.
  echo Da xuat output.docx
)
pause
