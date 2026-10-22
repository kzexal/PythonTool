from openpyxl import load_workbook
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
MODEL_NAME = "Japanese Vocabulary Model++"
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
            try:
                result = anki_request("addNotes", {
                    "notes": [{
                        "deckName": DECK_NAME,
                        "modelName": MODEL_NAME,
                        "fields": fields,
                        "tags": word["Tags"],
                    }]
                })

            except RuntimeError as exc:
                if "cannot create note because it is a duplicate" in str(exc).lower():
                    log(
                        f"BO QUA TU TRUNG: "
                        f"Japanese={word['Japanese']!r}, "
                        f"Reading={word['Reading']!r}. "
                        f"Can kiem tra ghi chu da co trong Anki."
                    )
                    continue

                raise

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





EXTRA_SHEETS = {
    
    "Grammar": {
        "deck": "Japanese Grammar",
        "model": "Japanese Grammar Model",
        "key": "Grammar",
        "fields": [
            "Grammar", "Meaning", "Structure",
            "Example", "ExampleMeaning", "JLPT", "Notes",
            "Front", "Back"
        ],
         "headers": [
            "Grammar", "Meaning", "Structure",
            "Example", "ExampleMeaning", "JLPT",
            "Notes", "Tags", "Front", "Back"
        ],
        "front": "{{Front}}",
        "back": "{{Back}}",
    },


    "Kanji": {
        "deck": "Japanese Kanji",
        "model": "Japanese Kanji Model",
        "key": "Kanji",
        "fields": [
            "Kanji", "Onyomi", "Kunyomi", "Meaning",
            "Radical", "StrokeCount", "ExampleWords", "Notes", "JLPT"
        ],
        "headers": [
            "Kanji", "Onyomi", "Kunyomi", "Meaning",
            "Radical", "StrokeCount", "ExampleWords",
            "Notes", "JLPT", "Tags"
        ],
        "front": "{{Kanji}}",
        "back": (
            "{{FrontSide}}<hr id=answer>"
            "{{Meaning}}<br>"
            "On: {{Onyomi}}<br>"
            "Kun: {{Kunyomi}}<br>"
            "Radical: {{Radical}}<br>"
            "Stroke count: {{StrokeCount}}<br>"
            "Examples: {{ExampleWords}}<br>"
            "{{Notes}}<br>{{JLPT}}"
        ),
    },
}


def read_settings(workbook):
    defaults = {
        "AnkiConnectUrl": "http://127.0.0.1:8765",
        "VocabularyDeck": "Japanese Vocabulary",
        "VocabularyModel": "Japanese Vocabulary Model",
        "GrammarDeck": "Japanese Grammar",
        "GrammarModel": "Japanese Grammar Model",
        "KanjiDeck": "Japanese Kanji",
        "KanjiModel": "Japanese Kanji Model",
        "Version": "1.0",
    }

    if "Settings" not in workbook.sheetnames:
        return defaults

    sheet = workbook["Settings"]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if len(row) >= 2 and row[0] is not None:
            key = str(row[0]).strip()
            value = row[1]
            if key in defaults and value is not None:
                defaults[key] = str(value).strip()

    return defaults


def ensure_extra_model(model_name, fields, front, back):
    model_names = anki_request("modelNames") or []

    if model_name not in model_names:
        anki_request("createModel", {
            "modelName": model_name,
            "inOrderFields": fields,
            "isCloze": False,
            "cardTemplates": [{
                "Name": "Card 1",
                "Front": front,
                "Back": back,
            }],
        })
        log(f"Da tao loai ghi chu '{model_name}'.")

    actual_fields = anki_request(
        "modelFieldNames",
        {"modelName": model_name}
    ) or []

    missing = [field for field in fields if field not in actual_fields]

    if missing:
        raise RuntimeError(
            f"Loai ghi chu '{model_name}' thieu truong: "
            + ", ".join(missing)
            + ". Khong tu dong sua model de tranh anh huong du lieu cu."
        )


def read_extra_rows(workbook, sheet_name, required_fields):
    if sheet_name not in workbook.sheetnames:
        log(f"Bo qua sheet '{sheet_name}': khong tim thay sheet.")
        return []

    sheet = workbook[sheet_name]

    if sheet.max_row < 2:
        return []

    headers = [
        str(cell.value).strip() if cell.value is not None else ""
        for cell in sheet[1]
    ]

    missing = [name for name in required_fields if name not in headers]

    if missing:
        raise RuntimeError(
            f"Sheet '{sheet_name}' thieu cot: " + ", ".join(missing)
        )

    rows = []

    for values in sheet.iter_rows(min_row=2, values_only=True):
        raw = dict(zip(headers, values))

        # Bo qua dong trong hoac khong co khoa dinh danh.
        key_value = raw.get(required_fields[0])
        if key_value is None or not str(key_value).strip():
            continue

        item = {}
        for name in headers:
            value = raw.get(name)
            item[name] = "" if value is None else str(value).strip()

        tags_text = item.get("Tags", "")
        item["Tags"] = main.parse_tags(tags_text) if tags_text else []

        rows.append(item)

    return rows


def sync_extra_sheet(workbook, sheet_name, config, deck_name, model_name):
    rows = read_extra_rows(
        workbook,
        sheet_name,
        [config["key"]]
    )

    if not rows:
        log(f"Sheet '{sheet_name}' khong co du lieu de dong bo.")
        return

    if deck_name not in (anki_request("deckNames") or []):
        anki_request("createDeck", {"deck": deck_name})
        log(f"Da tao bo the '{deck_name}'.")

    ensure_extra_model(
        model_name,
        config["fields"],
        config["front"],
        config["back"]
    )

    note_ids = anki_request(
        "findNotes",
        {"query": f'note:"{model_name}"'}
    ) or []

    existing_notes = []

    for start in range(0, len(note_ids), 200):
        existing_notes.extend(
            anki_request(
                "notesInfo",
                {"notes": note_ids[start:start + 200]}
            ) or []
        )

    by_key = {}

    for note in existing_notes:
        value = field_value(note, config["key"])
        normalized = main.normalize(value)
        by_key.setdefault(normalized, []).append(note)

    added = updated = unchanged = skipped = 0

    for row in rows:
        key = main.normalize(row.get(config["key"], ""))
        matches = by_key.get(key, [])

        if len(matches) > 1:
            skipped += 1
            log(
                f"BO QUA {sheet_name}: co nhieu ghi chu "
                f"cung khoa {config['key']}={row[config['key']]!r}."
            )
            continue

        fields = {
            name: main.html_escape(row.get(name, ""))
            for name in config["fields"]
        }

        if not matches:
            result = anki_request("addNotes", {
                "notes": [{
                    "deckName": deck_name,
                    "modelName": model_name,
                    "fields": fields,
                    "tags": row.get("Tags", []),
                }]
            })

            if result and result[0] is not None:
                added += 1
                by_key[key] = [{
                    "noteId": result[0],
                    "fields": {
                        name: {"value": fields[name]}
                        for name in config["fields"]
                    },
                    "tags": row.get("Tags", []),
                }]
            else:
                skipped += 1

            continue

        note = matches[0]
        note_id = note["noteId"]

        changed = {
            name: value
            for name, value in fields.items()
            if field_value(note, name) != value
        }

        if changed:
            anki_request("updateNoteFields", {
                "note": {
                    "id": note_id,
                    "fields": changed,
                }
            })
            updated += 1
        else:
            unchanged += 1

        current_tags = set(note.get("tags", []))
        new_tags = [
            tag for tag in row.get("Tags", [])
            if tag not in current_tags
        ]

        if new_tags:
            anki_request("addTags", {
                "notes": [note_id],
                "tags": " ".join(new_tags),
            })

    log(
        f"{sheet_name}: them {added}, cap nhat {updated}, "
        f"khong doi {unchanged}, bo qua {skipped}."
    )


def sync_grammar_and_kanji():
    excel_path = PROJECT_DIR / "input" / "vocabulary.xlsx"

    workbook = load_workbook(excel_path, data_only=True, read_only=True)

    try:
        settings = read_settings(workbook)

        for sheet_name in ("Grammar", "Kanji"):
            config = EXTRA_SHEETS[sheet_name]

            deck_name = settings.get(
                f"{sheet_name}Deck",
                config["deck"]
            )
            model_name = settings.get(
                f"{sheet_name}Model",
                config["model"]
            )

            sync_extra_sheet(
                workbook,
                sheet_name,
                config,
                deck_name,
                model_name
            )
    finally:
        workbook.close()


if __name__ == "__main__":
    try:
        main_sync()
        sync_grammar_and_kanji()
    except Exception as exc:
        try:
            log(f"LOI DONG BO: {type(exc).__name__}: {exc}")
        except Exception:
            pass



