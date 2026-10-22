from pathlib import Path
from datetime import datetime
import json
import time
import urllib.request
import sys

PROJECT_DIR = Path(r"C:\Users\buidu\OneDrive\Máy tính\pythontool\JapaneseFlashcards")
sys.path.insert(0, str(PROJECT_DIR))

import main

ANKI_CONNECT_URL = "http://127.0.0.1:8765"
DECK_NAME = "Japanese Vocabulary"
MODEL_NAME = "Japanese Vocabulary Model"
FIELD_NAMES = [
    "Japanese", "Reading", "Vietnamese",
    "Example", "ExampleMeaning", "Notes"
]
OUTPUT_DIR = PROJECT_DIR / "output"
LOG_FILE = OUTPUT_DIR / "anki_sync.log"





def log(message):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}"

    # Ghi log bang UTF-8
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

    # In ra console; khong de loi console lam dung dong bo
    try:
        print(line, flush=True)
    except (UnicodeEncodeError, OSError):
        pass



def anki_request(action, params=None):
    payload = json.dumps({
        "action": action,
        "version": 6,
        "params": params or {}
    }, ensure_ascii=False).encode("utf-8")

    request = urllib.request.Request(
        ANKI_CONNECT_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request, timeout=5) as response:
        result = json.loads(response.read().decode("utf-8"))

    if result.get("error") is not None:
        raise RuntimeError(
            f"AnkiConnect '{action}': {result['error']}"
        )

    return result.get("result")


def wait_for_anki(timeout_seconds=60):
    deadline = time.time() + timeout_seconds
    last_error = None

    while time.time() < deadline:
        try:
            return anki_request("version")
        except Exception as exc:
            last_error = exc
            time.sleep(2)

    raise RuntimeError(
        f"Khong ket noi duoc AnkiConnect sau {timeout_seconds} giay. "
        f"Kiem tra Anki va add-on AnkiConnect. Chi tiet: {last_error}"
    )


def field_value(note, name):
    field = note.get("fields", {}).get(name, {})
    return field.get("value", "") if isinstance(field, dict) else ""


def make_fields(word):
    return {
        "Japanese": main.html_escape(word["Japanese"]),
        "Reading": main.html_escape(word["Reading"]),
        "Vietnamese": main.html_escape(word["Vietnamese"]),
        "Example": main.html_escape(word["Example"]),
        "ExampleMeaning": main.html_escape(word["ExampleMeaning"]),
        "Notes": main.html_escape(word["Notes"]),
    }


def identity(japanese, reading):
    return (
        main.normalize(japanese),
        main.normalize(reading)
    )


def main_sync():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    log("Bat dau dong bo Excel -> Anki.")

    version = wait_for_anki()
    log(f"Da ket noi AnkiConnect phien ban {version}.")

    words, issues, duplicate_count, invalid_count = main.read_excel()

    if not words:
        raise RuntimeError(
            "Khong co tu hop le trong Excel; dung dong bo de tranh thao tac nham."
        )

    deck_names = anki_request("deckNames") or []

    if DECK_NAME not in deck_names:
        anki_request("createDeck", {"deck": DECK_NAME})
        log(f"Da tao bo the '{DECK_NAME}'.")

    model_names = anki_request("modelNames") or []

    if MODEL_NAME not in model_names:
        raise RuntimeError(
            f"Khong tim thay loai ghi chu '{MODEL_NAME}'. "
            "Hay nhap file APKG cua du an vao Anki it nhat mot lan truoc."
        )

    actual_fields = anki_request(
        "modelFieldNames",
        {"modelName": MODEL_NAME}
    ) or []

    missing_fields = [
        name for name in FIELD_NAMES
        if name not in actual_fields
    ]

    if missing_fields:
        raise RuntimeError(
            "Loai ghi chu hien tai thieu truong: "
            + ", ".join(missing_fields)
        )

    note_ids = anki_request(
        "findNotes",
        {"query": f'note:"{MODEL_NAME}"'}
    ) or []

    existing_notes = []

    for start in range(0, len(note_ids), 200):
        existing_notes.extend(
            anki_request(
                "notesInfo",
                {"notes": note_ids[start:start + 200]}
            ) or []
        )

    by_identity = {}

    for note in existing_notes:
        key = identity(
            field_value(note, "Japanese"),
            field_value(note, "Reading")
        )
        by_identity.setdefault(key, []).append(note)

    added = updated = unchanged = ambiguous = 0

    for word in words:
        key = identity(
            word["Japanese"],
            word["Reading"]
        )

        fields = make_fields(word)
        matches = by_identity.get(key, [])

        if len(matches) > 1:
            ambiguous += 1
            log(
                f"BO QUA: co {len(matches)} ghi chu trung dinh danh "
                f"Japanese={word['Japanese']!r}, "
                f"Reading={word['Reading']!r}."
            )
            continue

        if not matches:
            result = anki_request("addNotes", {
                "notes": [{
                    "deckName": DECK_NAME,
                    "modelName": MODEL_NAME,
                    "fields": fields,
                    "tags": word["Tags"],
                }]
            })

            new_ids = result or []

            if not new_ids or new_ids[0] is None:
                log(
                    f"CANH BAO: Anki khong them duoc tu "
                    f"{word['Japanese']!r}; co the tu da ton tai."
                )
                continue

            added += 1

            by_identity[key] = [{
                "noteId": new_ids[0],
                "fields": {
                    name: {"value": fields[name]}
                    for name in FIELD_NAMES
                },
                "tags": list(word["Tags"]),
            }]

            continue

        note = matches[0]
        note_id = note["noteId"]

        old_fields = {
            name: field_value(note, name)
            for name in FIELD_NAMES
        }

        changed_fields = {
            name: value
            for name, value in fields.items()
            if old_fields.get(name, "") != value
        }

        if changed_fields:
            anki_request("updateNoteFields", {
                "note": {
                    "id": note_id,
                    "fields": changed_fields
                }
            })
            updated += 1
        else:
            unchanged += 1

        current_tags = set(note.get("tags", []))

        tags_to_add = [
            tag for tag in word["Tags"]
            if tag not in current_tags
        ]

        if tags_to_add:
            anki_request(
                "addTags",
                {
                    "notes": [note_id],
                    "tags": " ".join(tags_to_add)
                }
            )

    log(
        f"Hoan tat: them {added}, cap nhat {updated}, "
        f"khong doi {unchanged}, bo qua do trung trong Anki {ambiguous}."
    )

    log(
        f"Excel: {len(words)} tu hop le; "
        f"{duplicate_count} dong trung; "
        f"{invalid_count} dong bi bo qua; "
        f"{len(issues)} canh bao/loi kiem tra."
    )

    if issues:
        log(
            "Co canh bao tu buoc kiem tra Excel; "
            "xem output/import_report.txt."
        )

    log("Khong xoa ghi chu nao khoi Anki.")



if __name__ == "__main__":
    try:
        main_sync()
    except Exception as exc:
        try:
            log(f"LOI DONG BO: {type(exc).__name__}: {exc}")
        except Exception:
            pass


