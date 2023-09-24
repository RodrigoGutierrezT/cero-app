from typing import Optional
import fastapi

router = fastapi.APIRouter()

@router.get("/api/citas")
def citas():
    pass