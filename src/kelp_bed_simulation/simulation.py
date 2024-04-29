__author__ = "Jeremy Nelson"

import datetime
import json
import pathlib

from attrs import define, field

from kelp_drone.drone import Drone


@define
class Place:
    latitude: float
    longitude: float

@define
class Scenario:
    place: Place

@define
class Simulation:
    scenario: Scenario
    created_on: datetime = field(default=datetime.datetime.now(datetime.UTC)) 
    epochs: int = field(default=5)
    history: list = field(factory=[])
    


