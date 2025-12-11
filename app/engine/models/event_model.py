# app/engine/models/event_model.py
from pydantic import BaseModel
from typing import Any, Dict


class EventModel(BaseModel):
    event_id: str
    timestamp: int
    event_type: str
    payload: Dict[str, Any]
    prev_hash: str
    hash: str
    signature: str
    pubkey: str
