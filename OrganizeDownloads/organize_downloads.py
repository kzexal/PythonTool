
from pathlib import Path
import shutil
import sys

# ==================================================
# 1. CẤU HÌNH
# ==================================================

DOWNLOADS = Path.home() / "Downloads"

# True: chỉ xem trước, chưa di chuyển file
# False: thực sự di chuyển file
DRY_RUN = False


# ==================================================
# 2. PHÂN LOẠI THEO ĐUÔI FILE
# ==================================================

FILE_TYPES = {
    "Tai_lieu": {
        ".pdf", ".doc", ".docx", ".txt", ".rtf",
        ".odt", ".ppt", ".pptx", ".xls", ".xlsx",
        ".csv", ".md"
    },

    "Hinh_anh": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        ".webp", ".svg", ".tiff", ".tif", ".raw",
        ".heic", ".ico"
    },

    "Video": {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv",
        ".flv", ".webm", ".m4v"
    },

    "Am_thanh": {
        ".mp3", ".wav", ".flac", ".aac", ".ogg",
        ".m4a", ".wma", ".opus"
    },

    "File_nen": {
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".bz2", ".xz"
    },

    "Cai_dat": {
        ".exe", ".msi", ".msix", ".apk", ".deb",
        ".rpm"
    },

    "Ma_nguon": {
        ".py", ".cs", ".java", ".cpp", ".c", ".h",
        ".js", ".ts", ".html", ".css", ".sql",
        ".json", ".xml", ".yaml", ".yml"
    }
}


# ==================================================
# 3. XÁC ĐỊNH THƯ MỤC ĐÍCH
# ==================================================

def get_category(file_path):
    extension = file_path.suffix.lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return "Khac"


# ==================================================
# 4. TRÁNH GHI ĐÈ FILE CÙNG TÊN
# ==================================================

def get_unique_path(destination):
    if not destination.exists():
        return destination

    folder = destination.parent
    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        candidate = folder / f"{stem}_{counter}{suffix}"

        if not candidate.exists():
            return candidate

        counter += 1


# ==================================================
# 5. SẮP XẾP FILE
# ==================================================

def organize_downloads():
    if not DOWNLOADS.is_dir():
        print(f"Khong tim thay thu muc: {DOWNLOADS}")
        return

    files = [
        path for path in DOWNLOADS.iterdir()
        if path.is_file()
    ]

    moved_count = 0
    skipped_count = 0

    print(f"Thu muc: {DOWNLOADS}")
    print(f"Che do xem truoc: {DRY_RUN}")
    print("-" * 50)

    for file_path in files:
        category = get_category(file_path)
        target_folder = DOWNLOADS / category
        destination = get_unique_path(
            target_folder / file_path.name
        )

        if DRY_RUN:
            print(
                f"[XEM TRUOC] {file_path.name}"
                f" -> {category}/{destination.name}"
            )
            moved_count += 1
            continue

        try:
            target_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            # Kiểm tra lại tên đích trước khi di chuyển
            destination = get_unique_path(
                target_folder / file_path.name
            )

            shutil.move(
                str(file_path),
                str(destination)
            )

            print(
                f"[DA CHUYEN] {file_path.name}"
                f" -> {category}/{destination.name}"
            )

            moved_count += 1

        except OSError as error:
            print(f"[LOI] {file_path.name}: {error}")
            skipped_count += 1

    print("-" * 50)
    print(f"So file du kien/da chuyen: {moved_count}")
    print(f"So file loi: {skipped_count}")

    if DRY_RUN:
        print("Chua co file nao bi di chuyen.")
        print("Hay doi DRY_RUN = False de thuc hien.")


if __name__ == "__main__":
    organize_downloads()
sys.exit(0)
