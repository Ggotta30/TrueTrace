from fastapi import APIRouter

from app.engine.chain.chain_reader import get_all_events, get_latest_event

router = APIRouter(tags=["events-read"])


@router.get("/latest")
def read_latest():
    return get_latest_event()


@router.get("/all")
def read_all_events():
    return get_all_events()
