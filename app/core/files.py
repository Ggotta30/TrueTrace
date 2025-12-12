import json
from pathlib import Path
from typing import Any, List

# ------------------------------------------------------------
# JSON LOADERS
# ------------------------------------------------------------


def load_json_file(path: str | Path) -> Any:
    """Load JSON from a file path."""
    path = Path(path)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# Backwards compatibility
load_json = load_json_file


# ------------------------------------------------------------
# JSON WRITERS
# ------------------------------------------------------------


def write_json(path: str | Path, data: Any) -> None:
    """Write JSON to a file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ------------------------------------------------------------
# UTILS
# ------------------------------------------------------------


def list_json_files_sorted(directory: str | Path) -> List[Path]:
    """Return all JSON files sorted alphabetically."""
    directory = Path(directory)
    if not directory.exists():
        return []
    return sorted(directory.glob("*.json"))
