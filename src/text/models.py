import uuid

from pydantic import UUID4, BaseModel, Field, Strict
from typing_extensions import Annotated


class GenerateTextIn(BaseModel):
    # https://github.com/pydantic/pydantic/discussions/7023
    session_id: Annotated[UUID4, Strict(False)]
    message: str


class GenerateTextOut(BaseModel):
    session_id: Annotated[UUID4, Strict(False)]
    message: str
