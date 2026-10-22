"""Xóa file cũ trong thư mục Temp của người dùng (%TEMP%).

Cách dùng:
    python clean_temp.py --dry-run      # chỉ liệt kê, không xóa (nên chạy thử trước)
    python clean_temp.py                # xóa file cũ hơn 3 ngày
    python clean_temp.py --days 7       # xóa file cũ hơn 7 ngày

File đang được chương trình khác dùng sẽ tự động bị bỏ qua.
"""
import argparse
import logging
import os
import tempfile
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE = Path(__file__).resolve().parent
LOG_FILE = BASE / "clean_temp.log"


def setup_logging(also_print):
    handlers = [RotatingFileHandler(LOG_FILE, maxBytes=512_000, backupCount=2, encoding="utf-8")]
    if also_print:
        handlers.append(logging.StreamHandler())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=handlers,
    )


def clean(temp_dir, max_age_days, dry_run):
    cutoff = time.time() - max_age_days * 86400
    deleted = skipped = freed = 0

    # topdown=False: xử lý file trước, rồi mới dọn thư mục rỗng
    for root, dirs, files in os.walk(temp_dir, topdown=False, followlinks=False):
        for name in files:
            path = os.path.join(root, name)
            try:
                if os.path.islink(path):
                    continue
                st = os.stat(path)
                if st.st_mtime > cutoff:
                    continue
                if dry_run:
                    logging.info("[dry-run] sẽ xóa: %s", path)
                else:
                    os.remove(path)
                deleted += 1
                freed += st.st_size
            except OSError:  # đang được dùng / không đủ quyền
                skipped += 1

        for name in dirs:
            path = os.path.join(root, name)
            try:
                if os.path.islink(path) or os.stat(path).st_mtime > cutoff:
                    continue
                if not dry_run:
                    os.rmdir(path)  # chỉ xóa được khi thư mục rỗng
            except OSError:
                pass  # không rỗng hoặc đang dùng -> bỏ qua

    return deleted, skipped, freed


def main():
    parser = argparse.ArgumentParser(description="Dọn file cũ trong thư mục Temp")
    parser.add_argument("--days", type=int, default=3, help="xóa file cũ hơn N ngày (mặc định 3)")
    parser.add_argument("--dry-run", action="store_true", help="chỉ liệt kê, không xóa")
    args = parser.parse_args()

    setup_logging(also_print=args.dry_run)
    temp_dir = tempfile.gettempdir()
    logging.info("Bắt đầu dọn %s (cũ hơn %d ngày)%s",
                 temp_dir, args.days, " [dry-run]" if args.dry_run else "")

    deleted, skipped, freed = clean(temp_dir, args.days, args.dry_run)
    logging.info("Xong: %d file, giải phóng %.1f MB, bỏ qua %d file đang dùng",
                 deleted, freed / 1_048_576, skipped)


if __name__ == "__main__":
    main()
