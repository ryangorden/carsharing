from fastapi import FastAPI, HTTPException
from schemas import load_db, save_db, CarInput, CarOutput, TripOutput, TripInput
import uvicorn

app = FastAPI()

db = load_db()


@app.get("/api/cars")
# when adding "doors: int" is called a type hint. allows us to add a hint to our function argument.
# this hint is ignored by python act like a comment. tool or modules can use this hint.
# good practice to add type hint where ever you can.
# "-> List" is specifing the type of return value for the function.
# "int|None" states we allow none or int. valid for python version 3.10 and up
# for python version less than 3.10 use "doors: Optional[str] = None"
# also for python version less than 3.10 List must be used instead of list for return value. The type 
# hints has to be imported as well.
def get_cars(doors: int | None = None, size: str | None = None) -> list:
    result = db
    if size:
        result = [car for car in db if car.size == size]
    if doors:
        result = [car for car in db if int(car.doors) >= int(doors)]
    return result


@app.get("/api/cars/{id}")
def car_by_id(id: int) -> dict:
    result = [car for car in db if car.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"No car found with id: {id}")


# uses response will tell the api doc how we expect the output of data to look
@app.post("/api/cars", response_model=CarOutput, status_code=201)
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors,
                        fuel=car.fuel, transmission=car.transmission,
                        id=len(db) + 1)
    db.append(new_car)
    save_db(db)
    return new_car


@app.delete("/api/cars/{id}", status_code=204)
def remove_care(id: int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.put("/api/cars/{id}", response_model=CarOutput)
def change_car(id: int, new_data: CarInput) -> CarOutput:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"NO car with id: {id}.")


@app.post("/api/cars/{car_id}/trips", response_model=TripOutput)
def add_trip(car_id: int, trip: TripInput) -> TripOutput:
    matches = [car for car in db if car.id == car_id]
    if matches:
        car = matches[0]
        new_trip = TripOutput(id=len(car.trips) + 1,
                              start=trip.start, end=trip.end,
                              description=trip.description)
        print(new_trip)
        car.trips.append(new_trip)
        save_db(db)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id: {id}.")


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
