import uvicorn
from fastapi import FastAPI, Body, status
from starlette.responses import JSONResponse

from flights.flight import Flight
from flights.flights_service import FlightService

app = FastAPI()
flight_service = FlightService("flights.csv")


@app.get("/{flight_id}")
async def get_flight(flight_id: str):
    if len(flight_id) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Flight ID cannot be empty")
    return JSONResponse(status_code=status.HTTP_200_OK, content=flight_service.get_flight(flight_id))


@app.post("/")
async def add_flight(flight: Flight = Body()):
    if len(flight.flight_id) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Flight ID cannot be empty")

    if flight_service.does_flight_exists(flight.flight_id):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Flight ID already exists")

    flight_service.append_flight(flight)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
