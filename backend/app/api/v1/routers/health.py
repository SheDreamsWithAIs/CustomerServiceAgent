from fastapi import APIRouter


router = APIRouter(tags=["health"], prefix="/health")


@router.get("", summary="Health check")
def read_health() -> dict:
    """Simple health endpoint to verify the API is up."""
    return {
        "status": "ok",
        "service": "office-lifeline",
        "version": "v1",
    }


