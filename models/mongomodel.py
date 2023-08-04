from typing import Annotated, Any, Literal

from bson import ObjectId
from fastapi.types import IncEx
from pydantic import BaseModel, Field, AliasChoices
from pydantic import PlainValidator, PlainSerializer


def objectId_validation(v: Any):
    try:
        return ObjectId(v)
    except:
        return None


def objectId_serialization_json(v):
    return str(v)


PydanticObjectId = Annotated[ObjectId, PlainValidator(objectId_validation), PlainSerializer(
    objectId_serialization_json, return_type=str, when_used="json")]


class MongoModel(BaseModel):
    id: PydanticObjectId = Field(None, validation_alias=AliasChoices("_id", "id"), alias="_id")

    def model_dump(
            self,
            mode: Literal['json', 'python'] | str = 'python',
            include: IncEx = None,
            exclude: IncEx = None,
            by_alias: bool = True,
            exclude_unset: bool = True,
            exclude_defaults: bool = False,
            exclude_none: bool = True,
            round_trip: bool = False,
            warnings: bool = True,
    ) -> dict[str, Any]:
        return super().model_dump(
            mode=mode,
            by_alias=by_alias,
            include=include,
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings, )

    def model_dump_json(
            self,
            *,
            indent: int | None = None,
            include: IncEx = None,
            exclude: IncEx = None,
            by_alias: bool = True,
            exclude_unset: bool = True,
            exclude_defaults: bool = True,
            exclude_none: bool = True,
            round_trip: bool = False,
            warnings: bool = True,
    ) -> str:
        return super().model_dump_json(
            indent=indent,
            by_alias=by_alias,
            include=include,
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings, )
