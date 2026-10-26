
import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import main


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
EXCEL_FILE = INPUT_DIR / "vocabulary.xlsx"

# Chờ Excel lưu xong trước khi xử lý
DEBOUNCE_SECONDS = 2

timer = None
timer_lock = threading.Lock()
build_lock = threading.Lock()


def build_flashcards():
    """Chạy lại quy trình xử lý Excel và xuất APKG."""

    # Tránh chạy nhiều lần đồng thời
    if not build_lock.acquire(blocking=False):
        print("[INFO] Đang tạo APKG, bỏ qua lần gọi trùng.")
        return

    try:
        print("\n" + "=" * 55)
        print("[INFO] Phát hiện thay đổi trong Excel.")
        print("[INFO] Bắt đầu kiểm tra dữ liệu và tạo APKG...")

        if not EXCEL_FILE.exists():
            print(f"[ERROR] Không tìm thấy file: {EXCEL_FILE}")
            return

        # Gọi lại quy trình của giai đoạn 1
        main.main()

        print("[INFO] Đã chạy xong quy trình giai đoạn 1.")

    except Exception as error:
        print(f"[ERROR] Không thể xử lý Excel: {error}")

    finally:
        build_lock.release()


def schedule_build():
    """Gộp nhiều sự kiện lưu file thành một lần xử lý."""

    global timer

    with timer_lock:
        if timer is not None:
            timer.cancel()

        timer = threading.Timer(
            DEBOUNCE_SECONDS,
            build_flashcards
        )
        timer.daemon = True
        timer.start()


class ExcelHandler(FileSystemEventHandler):
    def _is_target_file(self, path):
        if not path:
            return False

        try:
            return Path(path).resolve() == EXCEL_FILE.resolve()
        except (OSError, ValueError):
            return False

    def on_modified(self, event):
        if not event.is_directory and self._is_target_file(
            event.src_path
        ):
            print("[INFO] File Excel vừa được sửa.")
            schedule_build()

    def on_created(self, event):
        if not event.is_directory and self._is_target_file(
            event.src_path
        ):
            print("[INFO] File Excel vừa được tạo.")
            schedule_build()

    def on_moved(self, event):
        if not event.is_directory and (
            self._is_target_file(event.src_path)
            or self._is_target_file(event.dest_path)
        ):
            print("[INFO] File Excel vừa được thay thế hoặc di chuyển.")
            schedule_build()


def main_watch():
    if not INPUT_DIR.exists():
        print(f"[ERROR] Không tìm thấy thư mục: {INPUT_DIR}")
        return

    if not EXCEL_FILE.exists():
        print(f"[ERROR] Không tìm thấy file: {EXCEL_FILE}")
        print("Hãy đặt vocabulary.xlsx vào thư mục input.")
        return

    observer = Observer()
    observer.schedule(
        ExcelHandler(),
        str(INPUT_DIR),
        recursive=False
    )

    observer.start()

    print("=" * 55)
    print(" JAPANESE FLASHCARDS - EXCEL WATCHER")
    print("=" * 55)
    print(f"Đang theo dõi: {EXCEL_FILE}")
    print("Hãy chỉnh sửa và lưu file Excel để tự tạo APKG.")
    print("Nhấn Ctrl+C để dừng chương trình.")
    print("=" * 55)

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[INFO] Đang dừng chương trình...")

    finally:
        with timer_lock:
            if timer is not None:
                timer.cancel()

        observer.stop()
        observer.join()
        print("[INFO] Đã dừng theo dõi.")


if __name__ == "__main__":
    main_watch()
