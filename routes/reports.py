from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

