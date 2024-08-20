import uuid

from pydantic import UUID4, BaseModel, Field, Strict
from typing_extensions import Annotated


class GenerateTextIn(BaseModel):
    # https://github.com/pydantic/pydantic/discussions/7023
    session_id: Annotated[UUID4, Strict(False)] = Field(
        default_factory=uuid.uuid4, hidden=True
    )
    message: str

    class Config:
        @staticmethod
        def json_schema_extra(schema, model):
            if "properties" in schema:
                schema["properties"].pop("session_id", None)


class GenerateTextOut(BaseModel):
    session_id: Annotated[UUID4, Strict(False)]
    message: str
