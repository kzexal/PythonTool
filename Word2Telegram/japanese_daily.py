"""Gửi N từ vựng tiếng Nhật mỗi ngày qua Telegram, đọc từ file Excel.

Cần cài 1 lần:  pip install openpyxl

File Excel được đọc lại MỖI LẦN chạy, nên thêm/sửa/xóa từ trong Excel
(nhớ bấm Save) thì sáng hôm sau script tự cập nhật theo.

Cột bắt buộc ở dòng 1: Japanese | Reading | Vietnamese
Cột tùy chọn:          Example | ExampleMeaning   (thứ tự cột không quan trọng)
"""
import html
import json
import logging
import random
import urllib.parse
import urllib.request
from pathlib import Path

import openpyxl

BASE = Path(__file__).resolve().parent
CONFIG_FILE = BASE / "config.json"
STATE_FILE = BASE / "state.json"  # nhớ những từ đã gửi trong vòng hiện tại
LOG_FILE = BASE / "japanese_daily.log"

DEFAULT_EXCEL = "vocabulary.xlsx"  # có thể đổi bằng "excel_file" trong config.json
WORDS_PER_DAY = 5
RANDOM_ORDER = False  # True = chọn ngẫu nhiên; False = theo thứ tự trong file

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)


# ---------- Đọc Excel ----------
def load_vocab(excel_path, sheet_name=None):
    wb = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
    try:
        ws = wb[sheet_name] if sheet_name else wb.active
        rows = ws.iter_rows(values_only=True)
        header = next(rows, None)
        if not header:
            raise ValueError("File Excel trống")

        col = {str(h).strip().lower(): i for i, h in enumerate(header) if h is not None}
        for need in ("japanese", "reading", "vietnamese"):
            if need not in col:
                raise ValueError(f"Thiếu cột '{need}' ở dòng đầu tiên của file Excel")

        def get(row, name):
            i = col.get(name)
            if i is None or i >= len(row) or row[i] is None:
                return ""
            return str(row[i]).strip()

        vocab = []
        for row in rows:
            word = get(row, "japanese")
            if not word:
                continue  # bỏ dòng trống
            reading = get(row, "reading")
            vocab.append({
                "key": f"{word}|{reading}",  # định danh từ, không phụ thuộc số dòng
                "word": word,
                "reading": reading,
                "meaning": get(row, "vietnamese"),
                "example": get(row, "example"),
                "example_meaning": get(row, "examplemeaning"),
            })
        return vocab
    finally:
        wb.close()


# ---------- Trạng thái ----------
def load_state():
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return set(data.get("sent", [])), int(data.get("cycle", 1))
    except (OSError, ValueError, TypeError):
        return set(), 1


def save_state(sent, cycle):
    STATE_FILE.write_text(
        json.dumps({"cycle": cycle, "sent": sorted(sent)}, ensure_ascii=False),
        encoding="utf-8",
    )


# ---------- Chọn từ ----------
def pick_words(vocab, sent, cycle, n, randomize):
    """Chọn n từ CHƯA gửi trong vòng hiện tại. Hết từ thì sang vòng mới."""
    n = min(n, len(vocab))
    pool = [w for w in vocab if w["key"] not in sent]
    if randomize:
        random.shuffle(pool)
    picked = pool[:n]

    if len(picked) < n:  # không đủ từ mới -> bắt đầu vòng mới, bù thêm
        cycle += 1
        taken = {w["key"] for w in picked}
        extra = [w for w in vocab if w["key"] not in taken]
        if randomize:
            random.shuffle(extra)
        extra = extra[: n - len(picked)]
        picked += extra
        sent = {w["key"] for w in extra}
    else:
        sent = sent | {w["key"] for w in picked}
    return picked, sent, cycle


# ---------- Tin nhắn ----------
def build_message(words, learned, total, cycle):
    lines = [f"🌸 <b>{len(words)} từ tiếng Nhật hôm nay</b>  (vòng {cycle}: {learned}/{total})\n"]
    for i, w in enumerate(words, 1):
        e = html.escape
        lines.append(f"{i}. <b>{e(w['word'])}</b> ({e(w['reading'])}) — <tg-spoiler>{e(w['meaning'])}</tg-spoiler>")
        if w["example"]:
            lines.append(f"    例: {e(w['example'])}")
            if w["example_meaning"]:
                lines.append(f"    <tg-spoiler>{e(w['example_meaning'])}</tg-spoiler>")
        lines.append("")
    return "\n".join(lines).strip()


def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode(
        {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    ).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=30) as resp:
        resp.read()


def main():
    config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    excel_path = Path(config.get("excel_file") or DEFAULT_EXCEL)
    if not excel_path.is_absolute():
        excel_path = BASE / excel_path

    vocab = load_vocab(excel_path, config.get("sheet_name"))
    if not vocab:
        raise SystemExit("Không có từ nào trong file Excel")

    sent, cycle = load_state()
    sent &= {w["key"] for w in vocab}  # bỏ những từ đã bị xóa khỏi file

    words, sent, cycle = pick_words(vocab, sent, cycle, WORDS_PER_DAY, RANDOM_ORDER)
    text = build_message(words, len(sent), len(vocab), cycle)
    send_telegram(config["bot_token"], config["chat_id"], text)
    save_state(sent, cycle)  # chỉ lưu khi gửi thành công
    logging.info("Đã gửi %d từ (vòng %d, %d/%d)", len(words), cycle, len(sent), len(vocab))


if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        logging.error("Không đọc được file Excel (đang mở/khóa?). Sẽ thử lại lần chạy sau.")
        raise
    except Exception:
        logging.exception("Lỗi khi gửi từ vựng")
        raise