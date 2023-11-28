from typing import Annotated

from fastapi import APIRouter, Depends

from db import equation_get_many
from security import get_current_active_user, get_optional_user
from api.models import *
router = APIRouter(prefix="/equation")


@router.get("/", response_model=Response[Equation])
async def get(current_user: Annotated[User, Depends(get_optional_user)], id: str, limit: int, skip: int):

    result = await equation_get_many(query_string=id, n_results=limit,
                                     skip=skip)
    return result

