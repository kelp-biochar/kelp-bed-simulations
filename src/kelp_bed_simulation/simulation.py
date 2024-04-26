__author__ = "Jeremy Nelson"

import json
import pathlib

from attrs import define, field

from kelp_drone.drone import Drone

@define
class Simulation:
    epochs: int = field(default=5)
    history: list = field(factory=[])


