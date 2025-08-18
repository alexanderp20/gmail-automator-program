from pathlib import Path
import json, sys
from gmail_sender import run_batch

# Paths
SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent
DATA_DIR = ROOT_DIR / "data"   # where body.html/body.txt/recipients.txt/requirements.txt live
CONFIG_PATH = SRC_DIR / "config.json"


def load_config(path: Path):
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"Config not found: {path}")
    except Exception as e:
        sys.exit(f"Failed to parse config.json: {e}")

    if not cfg.get("recipients_file"):
        sys.exit("Missing `recipients_file` in config.json")
    if not cfg.get("subject"):
        sys.exit("Missing `subject` in config.json")
    if not cfg.get("body") and not cfg.get("body_file"):
        sys.exit("Provide either `body` or `body_file` in config.json")
    return cfg


def resolve_in_data(filename_or_path: str) -> Path:
    """Return a Path under data/ unless an absolute path is given."""
    p = Path(filename_or_path)
    return p if p.is_absolute() else (DATA_DIR / p)


def main():
    cfg = load_config(CONFIG_PATH)

    # Load body from body_file (under data/) unless inline `body` provided
    body_text = cfg.get("body")
    body_file = cfg.get("body_file")
    if body_text is None and body_file:
        body_path = resolve_in_data(body_file)
        try:
            body_text = body_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            sys.exit(f"Body file not found: {body_path}")

    # Recipients path resolves inside data/
    recipients_path = resolve_in_data(cfg["recipients_file"])

    # HTML if config says so OR file extension is .html
    html = bool(cfg.get("html", False)) or str(cfg.get("body_file", "")).lower().endswith(".html")

    run_batch(
        recipients_path=recipients_path,
        subject=cfg["subject"],
        body=body_text,
        html=html,
        from_name=cfg.get("from_name"),
        sleep=float(cfg.get("sleep", 0.5)),
        dry=bool(cfg.get("dry", False)),
    )


if __name__ == "__main__":
    main()