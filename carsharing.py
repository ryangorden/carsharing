from fastapi import FastAPI, HTTPException
import uvicorn


app = FastAPI()

db = [{"id": 1, "size": "s", "fuel": "gas", "doors": "3", "transmission": "auto"},
    {"id": 2, "size": "s", "fuel": "ele", "doors": "3", "transmission": "auto"},
    {"id": 3, "size": "s", "fuel": "gas", "doors": "5", "transmission": "manual"},
    {"id": 4, "size": "m", "fuel": "ele", "doors": "3", "transmission": "auto"},
    {"id": 5, "size": "m", "fuel": "hyb", "doors": "5", "transmission": "auto"},
    {"id": 6, "size": "m", "fuel": "gas", "doors": "3", "transmission": "manual"},
    {"id": 7, "size": "l", "fuel": "dies", "doors": "5", "transmission": "manual"},
    {"id": 8, "size": "l", "fuel": "ele", "doors": "5", "transmission": "auto"},
    {"id": 9, "size": "l", "fuel": "hyb", "doors": "5", "transmission": "auto"},
      ]



@app.get("/api/cars")
# when adding "doors: int" is called a type hint. allows us to add a hint to our function argument.
# this hint is ignored by python act like a comment. tool or modules can use this hint.
# good practice to add type hint where ever you can.
# "-> List" is specifing the type of return value for the function.
# "int|None" states we allow none or int. valid for python version 3.10 and up
# for python version less than 3.10 use "doors: Optional[str] = None"
# also for python version less than 3.10 List must be used instead of list for return value. The type 
# hints has to be imported as well.
def get_cars(doors: int|None = None, size: str|None = None) -> list:
    result = db
    if size:
        result= [car for car in db if car["size"] == size]
    if doors:
        result= [car for car in db if int(car["doors"]) >= int(doors)]
    return result

@app.get("/api/cars/{id}")
def car_by_id(id: int)-> dict:
    
    result = [car for car in db if car["id"] == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"No car found with id: {id}")

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
