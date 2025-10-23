from datetime import datetime, timezone
from enum import Enum
from typing import Mapping

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class AttractionState(str, Enum):
    Ouvert = "Ouvert"
    Fermé = "Fermé"
    EnMaintenance = "En maintenance"


class Attraction(BaseModel):
    name: str
    status: AttractionState
    waitingTime: int


app = FastAPI()

app.state.attractions = [
    Attraction(name="Roller Coaster", status=AttractionState.Ouvert, waitingTime=30),
    Attraction(name="Ferris Wheel", status=AttractionState.Ouvert, waitingTime=15),
    Attraction(name="Haunted House", status=AttractionState.Fermé, waitingTime=0),
    Attraction(name="Water Slide", status=AttractionState.Ouvert, waitingTime=45),
    Attraction(name="Water Slide", status=AttractionState.Ouvert, waitingTime=45),
    Attraction(name="Carousel", status=AttractionState.Ouvert, waitingTime=10),
]
app.state.attraction_version = 1
app.state.attraction_last_modified = datetime.now(timezone.utc)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
)


@app.get("/attractions", response_model=list[Attraction])
def get_attractions(request: Request) -> Response:
    attractions = request.app.state.attractions

    # Compute ETag based on attractions data
    attraction_version = str(request.app.state.attraction_version)

    # Set a fixed Last-Modified date (since data is static)
    last_modified = app.state.attraction_last_modified.strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

    # Check for conditional requests
    if_none_match = request.headers.get("If-None-Match")
    if_modified_since = request.headers.get("If-Modified-Since")
    if if_none_match == attraction_version or (
        if_modified_since and if_modified_since == last_modified
    ):
        return Response(status_code=304)

    # Set response headers
    headers: Mapping[str, str] = {}
    headers["ETag"] = attraction_version
    headers["Last-Modified"] = last_modified
    headers["Cache-Control"] = "no-cache, must-revalidate"

    attractions_json = jsonable_encoder(attractions)
    return JSONResponse(content=attractions_json, headers=headers)


@app.post("/attractions/bump_version")
def bump_attraction_version(request: Request) -> dict[str, str]:
    request.app.state.attraction_version += 1
    request.app.state.attraction_last_modified = datetime.now(timezone.utc)
    formatted_last_modified = request.app.state.attraction_last_modified.strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    return {
        "attraction_version": request.app.state.attraction_version,
        "last_modified": formatted_last_modified,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
