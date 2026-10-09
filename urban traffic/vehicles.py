from dataclasses import dataclass


@dataclass
class VehicleType:
    name: str
    weight: float
    arrival_rate: float       # vehicles per second
    departure_rate: float     # vehicles per second


class Car(VehicleType):
    def __init__(self):
        super().__init__(
            name="car",
            weight=1.0,
            arrival_rate=0.80,
            departure_rate=0.60
        )


class Bike(VehicleType):
    def __init__(self):
        super().__init__(
            name="bike",
            weight=0.5,
            arrival_rate=0.60,
            departure_rate=0.90
        )


class SUV(VehicleType):
    def __init__(self):
        super().__init__(
            name="suv",
            weight=1.5,
            arrival_rate=0.30,
            departure_rate=0.40
        )


class Bus(VehicleType):
    def __init__(self):
        super().__init__(
            name="bus",
            weight=3.0,
            arrival_rate=0.08,
            departure_rate=0.20
        )