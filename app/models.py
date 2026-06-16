"""Pydantic models for the audience builder API."""
from pydantic import BaseModel, Field, model_validator


class AudienceFilters(BaseModel):
    min_age: int | None = Field(default=None, ge=0, le=120)
    max_age: int | None = Field(default=None, ge=0, le=120)

    @model_validator(mode="after")
    def check_age_range(self) -> "AudienceFilters":
        if (
            self.min_age is not None
            and self.max_age is not None
            and self.min_age > self.max_age
        ):
            raise ValueError("min_age must be <= max_age")
        return self


class AudienceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    filters: AudienceFilters


class Person(BaseModel):
    person_id: int
    age: int
    state: str
    first_name: str
    last_name: str


class Audience(BaseModel):
    id: int
    name: str
    filters: AudienceFilters
    size: int


class AudienceMembers(BaseModel):
    id: int
    members: list[Person]
