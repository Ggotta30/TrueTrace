import os
import json
from typing import Optional, List, Dict

from app.core.paths import EVENT_DB_FILE


class EventDB:
    """
    Simple file-based event database.
    Stores full event objects in JSONL format.
    """

    def __init__(self, db_path: str = EVENT_DB_FILE):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def add(self, event: Dict):
        """Append an event to the DB file."""
        with open(self.db_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    def list_all(self) -> List[Dict]:
        """Return all stored events."""
        if not os.path.exists(self.db_path):
            return []
        with open(self.db_path, "r", encoding="utf-8") as f:
            return [json.loads(line.strip()) for line in f if line.strip()]

    def latest(self) -> Optional[Dict]:
        """Return the most recent event or None."""
        events = self.list_all()
        return events[-1] if events else None


# Existing free functions preserved for compatibility
def add_event_db(event: Dict):
    db = EventDB()
    db.add(event)


def get_latest_event():
    db = EventDB()
    return db.latest()
