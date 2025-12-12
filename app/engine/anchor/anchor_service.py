# app/engine/anchor/anchor_service.py
"""
Scaffold for the Background Anchor Service.

This file provides a simple class you can wire to a background task runner (e.g. FastAPI startup event
that creates an asyncio Task). It currently does not perform external anchoring, only computes a Merkle root
placeholder and writes an 'anchor record' to event_chain.json when invoked.

Extend this to submit roots to a blockchain, timestamping service, or store receipts.
"""
import asyncio
import hashlib
import json
from pathlib import Path
from typing import List

EVENT_CHAIN_PATH = Path.cwd() / "event_chain.json"
ANCHOR_RECORD_KEY = "anchors"


class AnchorService:
    def __init__(self, interval_seconds: int = 60 * 60):
        self.interval = interval_seconds
        self._task = None
        self._running = False

    async def start(self):
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._loop())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _loop(self):
        while self._running:
            try:
                await self.perform_anchor()
            except Exception:
                # logging can be added here
                pass
            await asyncio.sleep(self.interval)

    async def perform_anchor(self):
        """
        Load chain, compute a simple merkle-like root (naive: hash of concatenated event hashes),
        and append an anchor record into the chain file (not into the canonical event chain).
        Replace with real Merkle tree and external submission later.
        """
        chain = self._load_chain()
        if not chain:
            return None
        hashes = [ev.get("hash", "") for ev in chain]
        concat = "".join(hashes).encode("utf-8")
        root = hashlib.sha256(concat).hexdigest()

        # write anchor metadata into event_chain.json as a top-level anchors list
        # Be conservative: preserve existing structure
        data = {}
        if EVENT_CHAIN_PATH.exists():
            try:
                with EVENT_CHAIN_PATH.open("r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        anchors = data.get(ANCHOR_RECORD_KEY, [])
        anchors.append({"root": root, "timestamp": int(__import__("time").time())})
        data[ANCHOR_RECORD_KEY] = anchors
        # preserve event list under "events" key if present on read
        if isinstance(data, dict) and "events" not in data:
            data["events"] = chain
        with EVENT_CHAIN_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return root

    def _load_chain(self) -> List[dict]:
        if not EVENT_CHAIN_PATH.exists():
            return []
        with EVENT_CHAIN_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "events" in data:
                return data["events"]
            return []
