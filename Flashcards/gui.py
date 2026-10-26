
import contextlib
import io
import queue
import subprocess
import threading
import tkinter as tk

from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import main
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_EXCEL = BASE_DIR / "input" / "vocabulary.xlsx"
OUTPUT_DIR = BASE_DIR / "output"

# Các thành phần giao tiếp giữa luồng nền và giao diện
ui_queue = queue.Queue()
observer = None
auto_build = False
debounce_id = None
is_building = False


def log(message):
    ui_queue.put(("log", message))


def set_status(message):
    ui_queue.put(("status", message))


def selected_path():
    return Path(excel_var.get()).expanduser().resolve()


def generate_apkg():
    """Tạo APKG trong luồng nền."""

    global is_building

    if is_building:
        log("[INFO] Đang xử lý, bỏ qua yêu cầu trùng.")
        return

    is_building = True
    set_status("Đang xử lý...")

    try:
        excel_path = selected_path()

        if not excel_path.is_file():
            raise FileNotFoundError(
                f"Không tìm thấy file Excel:\n{excel_path}"
            )

        log(f"\n[{datetime.now():%H:%M:%S}] Bắt đầu xử lý")
        log(f"Excel: {excel_path}")

        # main.py ở giai đoạn 1 dùng biến INPUT_FILE.
        # Cập nhật biến để dùng file đã chọn trên giao diện.
        main.INPUT_FILE = excel_path

        # Bắt nội dung print() từ main.py để hiển thị trên giao diện.
        buffer = io.StringIO()

        with contextlib.redirect_stdout(buffer):
            with contextlib.redirect_stderr(buffer):
                main.main()

        output = buffer.getvalue().strip()

        if output:
            log(output)

        # Hiển thị báo cáo nếu có.
        report_path = getattr(
            main,
            "REPORT_FILE",
            OUTPUT_DIR / "import_report.txt"
        )

        report_path = Path(report_path)

        if report_path.is_file():
            log("\n--- Báo cáo nhập liệu ---")
            log(report_path.read_text(encoding="utf-8-sig"))

        apkg_path = Path(
            getattr(
                main,
                "OUTPUT_FILE",
                OUTPUT_DIR / "Japanese_Vocabulary.apkg"
            )
        )

        if apkg_path.is_file():
            log(f"\n[INFO] File APKG hiện có: {apkg_path}")
            set_status("Đã hoàn tất")
        else:
            log("[ERROR] Không tìm thấy file APKG đầu ra.")
            set_status("Chưa tạo được APKG")

    except Exception as error:
        log(f"[ERROR] {error}")
        set_status("Có lỗi xảy ra")

    finally:
        is_building = False


def start_generation():
    """Chạy xử lý trong luồng riêng để giao diện vẫn phản hồi."""

    if is_building:
        messagebox.showinfo(
            "Đang xử lý",
            "Vui lòng đợi quá trình hiện tại hoàn tất."
        )
        return

    threading.Thread(
        target=generate_apkg,
        daemon=True
    ).start()


def on_excel_changed():
    """Chờ file ổn định trước khi tự tạo APKG."""

    global debounce_id

    if not auto_var.get():
        return

    if debounce_id is not None:
        root.after_cancel(debounce_id)

    debounce_id = root.after(1800, start_generation)


class ExcelHandler(FileSystemEventHandler):
    def __init__(self, target):
        self.target = target.resolve()

    def matches(self, path):
        if not path:
            return False

        try:
            return Path(path).resolve() == self.target
        except (OSError, ValueError):
            return False

    def on_modified(self, event):
        if not event.is_directory and self.matches(event.src_path):
            root.after(0, on_excel_changed)

    def on_created(self, event):
        if not event.is_directory and self.matches(event.src_path):
            root.after(0, on_excel_changed)

    def on_moved(self, event):
        if not event.is_directory and (
            self.matches(event.src_path)
            or self.matches(event.dest_path)
        ):
            root.after(0, on_excel_changed)


def stop_watcher():
    global observer

    if observer is not None:
        observer.stop()
        observer.join(timeout=3)
        observer = None


def update_watcher():
    """Bật hoặc tắt theo dõi file Excel đã chọn."""

    global observer, auto_build

    stop_watcher()
    auto_build = auto_var.get()

    if not auto_build:
        log("[INFO] Đã tắt tự động theo dõi.")
        return

    try:
        target = selected_path()

        if not target.is_file():
            auto_var.set(False)
            auto_build = False
            messagebox.showwarning(
                "Không tìm thấy file",
                "Hãy chọn một file Excel tồn tại trước khi bật theo dõi."
            )
            return

        new_observer = Observer()
        new_observer.schedule(
            ExcelHandler(target),
            str(target.parent),
            recursive=False
        )
        new_observer.start()
        observer = new_observer

        log(f"[INFO] Đang theo dõi: {target}")

    except Exception as error:
        auto_var.set(False)
        auto_build = False
        stop_watcher()
        messagebox.showerror("Lỗi theo dõi", str(error))


def choose_excel():
    path = filedialog.askopenfilename(
        title="Chọn file từ vựng Excel",
        initialdir=str(BASE_DIR / "input"),
        filetypes=[
            ("Excel workbook", "*.xlsx"),
            ("Tất cả file", "*.*")
        ]
    )

    if not path:
        return

    was_watching = auto_var.get()

    if was_watching:
        auto_var.set(False)
        update_watcher()

    excel_var.set(path)
    log(f"[INFO] Đã chọn file: {path}")

    if was_watching:
        auto_var.set(True)
        update_watcher()


def open_output_folder():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.Popen(["explorer", str(OUTPUT_DIR)])
    except OSError as error:
        messagebox.showerror("Lỗi", str(error))


def poll_queue():
    """Cập nhật giao diện từ các tác vụ nền."""

    try:
        while True:
            kind, value = ui_queue.get_nowait()

            if kind == "log":
                log_text.configure(state="normal")
                log_text.insert("end", str(value) + "\n")
                log_text.see("end")
                log_text.configure(state="disabled")

            elif kind == "status":
                status_var.set(value)

    except queue.Empty:
        pass

    root.after(150, poll_queue)


def close_app():
    global debounce_id

    if debounce_id is not None:
        root.after_cancel(debounce_id)

    stop_watcher()
    root.destroy()


# =========================
# GIAO DIỆN
# =========================

root = tk.Tk()
root.title("JapaneseFlashcards")
root.geometry("760x600")
root.minsize(620, 480)

style = ttk.Style(root)

if "vista" in style.theme_names():
    style.theme_use("vista")
elif "clam" in style.theme_names():
    style.theme_use("clam")

excel_var = tk.StringVar(value=str(DEFAULT_EXCEL))
auto_var = tk.BooleanVar(value=True)
status_var = tk.StringVar(value="Đang khởi động...")

container = ttk.Frame(root, padding=20)
container.pack(fill="both", expand=True)

ttk.Label(
    container,
    text="JapaneseFlashcards",
    font=("Segoe UI", 21, "bold")
).pack(anchor="w")

ttk.Label(
    container,
    text="Quản lý từ vựng tiếng Nhật và tạo bộ thẻ Anki",
    font=("Segoe UI", 10)
).pack(anchor="w", pady=(2, 18))

# Chọn Excel
ttk.Label(
    container,
    text="File Excel đầu vào",
    font=("Segoe UI", 10, "bold")
).pack(anchor="w")

file_frame = ttk.Frame(container)
file_frame.pack(fill="x", pady=(6, 14))

ttk.Entry(
    file_frame,
    textvariable=excel_var
).pack(side="left", fill="x", expand=True, padx=(0, 8))

ttk.Button(
    file_frame,
    text="Chọn file...",
    command=choose_excel
).pack(side="right")

# Các thao tác chính
action_frame = ttk.Frame(container)
action_frame.pack(fill="x", pady=(0, 12))

ttk.Button(
    action_frame,
    text="Kiểm tra và tạo APKG",
    command=start_generation
).pack(side="left", padx=(0, 8))

ttk.Button(
    action_frame,
    text="Mở thư mục kết quả",
    command=open_output_folder
).pack(side="left")

# Theo dõi tự động
ttk.Checkbutton(
    container,
    text="Tự động tạo APKG khi Excel thay đổi",
    variable=auto_var,
    command=update_watcher
).pack(anchor="w", pady=(2, 12))

# Trạng thái
status_frame = ttk.Frame(container)
status_frame.pack(fill="x", pady=(0, 6))

ttk.Label(
    status_frame,
    text="Trạng thái:"
).pack(side="left")

ttk.Label(
    status_frame,
    textvariable=status_var,
    font=("Segoe UI", 9, "bold")
).pack(side="left", padx=(6, 0))

# Nhật ký
ttk.Label(
    container,
    text="Nhật ký xử lý",
    font=("Segoe UI", 10, "bold")
).pack(anchor="w", pady=(4, 6))

log_frame = ttk.Frame(container)
log_frame.pack(fill="both", expand=True)

scrollbar = ttk.Scrollbar(log_frame)
scrollbar.pack(side="right", fill="y")

log_text = tk.Text(
    log_frame,
    height=12,
    wrap="word",
    font=("Consolas", 9),
    state="disabled",
    yscrollcommand=scrollbar.set
)
log_text.pack(side="left", fill="both", expand=True)
scrollbar.configure(command=log_text.yview)

ttk.Label(
    container,
    text="Đầu ra: output/Japanese_Vocabulary.apkg",
    font=("Segoe UI", 9)
).pack(anchor="w", pady=(10, 0))
root.protocol("WM_DELETE_WINDOW", close_app)

root.after(150, poll_queue)

# Tự động theo dõi vocabulary.xlsx khi mở ứng dụng
root.after(500, update_watcher)

root.mainloop()
