from fastapi import APIRouter
from app.engine.chain.chain_reader import get_all_events

router = APIRouter()


@router.get("/search")
def search_events(q: str):
    results = []

    for event in get_all_events():
        text = str(event)
        if q.lower() in text.lower():
            results.append(event)

    return {"query": q, "results": results}
