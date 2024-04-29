from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/cams",
    tags=["cams"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)