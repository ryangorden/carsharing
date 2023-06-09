import json
from pydantic import BaseModel


class TripInput(BaseModel):
    start: int
    end: int
    description: str


class TripOutput(TripInput):
    id: int


class CarInput(BaseModel):
    size: str
    fuel: str | None = "ele"
    doors: int
    transmission: str | None = "auto"

    # this class below help tool like postman model data of exaple
    # inputs of data when importing information
    class Config:
        schema_extra = {
            "example": {
                "size": "m",
                "doors": 5,
                "transmission": "auto",
                "fuel": "gas"
            }
        }


class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []


def load_db() -> list[CarOutput]:
    """Load a list of Car objects from json file"""
    with open("cars.json", "r") as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]


def save_db(cars: list[CarOutput]):
    with open("cars.json", "w") as f:
        json.dump([car.dict() for car in cars], f, indent=4)
