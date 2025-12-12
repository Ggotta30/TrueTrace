from fastapi import APIRouter

from .endpoints import diagnostics, events, events_read, health

router = APIRouter(prefix="/api/v1")

router.include_router(events.router, prefix="/events")
router.include_router(events_read.router, prefix="/events")
router.include_router(health.router, prefix="/health")
router.include_router(diagnostics.router, prefix="/diagnostics", tags=["diagnostics"])
