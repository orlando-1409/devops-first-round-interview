"""Audience Builder API.

Lets users create audiences by filtering on age, and retrieve the members
that match each audience definition.
"""
from itertools import count

from fastapi import FastAPI, HTTPException

from app.data import filter_people
from app.models import (
    Audience,
    AudienceCreate,
    AudienceMembers,
    Person,
)

app = FastAPI(title="Audience Builder API", version="0.1.0")

_audiences: dict[int, AudienceCreate] = {}
_id_seq = count(start=1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/audiences", response_model=Audience, status_code=201)
def create_audience(payload: AudienceCreate) -> Audience:
    audience_id = next(_id_seq)
    _audiences[audience_id] = payload
    matched = filter_people(
        min_age=payload.filters.min_age,
        max_age=payload.filters.max_age,
    )
    return Audience(
        id=audience_id,
        name=payload.name,
        filters=payload.filters,
        size=len(matched),
    )


@app.get("/audiences/{audience_id}", response_model=Audience)
def get_audience(audience_id: int) -> Audience:
    audience = _audiences.get(audience_id)
    if audience is None:
        raise HTTPException(status_code=404, detail="audience not found")
    matched = filter_people(
        min_age=audience.filters.min_age,
        max_age=audience.filters.max_age,
    )
    return Audience(
        id=audience_id,
        name=audience.name,
        filters=audience.filters,
        size=len(matched),
    )


@app.get("/audiences/{audience_id}/members", response_model=AudienceMembers)
def get_audience_members(audience_id: int) -> AudienceMembers:
    audience = _audiences.get(audience_id)
    if audience is None:
        raise HTTPException(status_code=404, detail="audience not found")
    matched = filter_people(
        min_age=audience.filters.min_age,
        max_age=audience.filters.max_age,
    )
    members = [Person(**row) for row in matched.to_dict(orient="records")]
    return AudienceMembers(id=audience_id, members=members)
