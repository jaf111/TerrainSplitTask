from fastapi import APIRouter

from app.models.error_model import error_responses_500


router = APIRouter()

@router.get(
    "/",
    responses={**error_responses_500}
)
async def health():
    # should check status of db as well 
    return {"Status": "UP"}