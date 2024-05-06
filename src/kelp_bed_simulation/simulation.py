__author__ = "Jeremy Nelson"

import json
import pathlib
import re

from datetime import datetime

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
    created_on: datetime 
    epochs: int = field(default=5)
    

def parse_buoy_data(data: str) -> dict:
    """
    Parses text from retrieving Buoy URLs like 
    https://www.ndbc.noaa.gov/data/latest_obs/46092.txt
    """
    # Regular expressions for each field
    station_id_pattern = r"Station (\d+)"
    latitude_pattern = r"(\d+)° (\d+\.\d+)' (\w)"
    longitude_pattern = r"(\d+)° (\d+\.\d+)' (\w)"
    time_pattern = r"(\d+):(\d+) (\w+) (\w+)"
    date_pattern = r"(\d+)/(\d+)/(\d+)"
    wind_pattern = r"Wind: (\w+) \((\d+)°\), (\d+\.\d+) kt"
    pressure_pattern = r"Pres: (\d+\.\d+) (\w+)"
    air_temp_pattern = r"Air Temp: (\d+\.\d+) °F"
    water_temp_pattern = r"Water Temp: (\d+\.\d+) °F"

    output = {
        "station_id": None,
        "latitude": None,
        "longitude": None,
        "date": None,
        "wind_direction": None,
        "wind_direction_deg": None,
        "wind_speed": None,
        "pressure": None,
        "pressure_tendency": None,
        "air_temp_c": None,
        "water_temp_c": None
        }
    
    # Match each field using the corresponding pattern
    station_id_match = re.search(station_id_pattern, data)
    if station_id_match:
        output["station_id"] = int(station_id_match.group(1))
    latitude_match = re.search(latitude_pattern, data)
    if latitude_match:
        latitude_degrees = float(latitude_match.group(1))
        latitude_minutes = float(latitude_match.group(2))
        latitude_dir = latitude_match.group(3)
        latitude = latitude_degrees + latitude_minutes / 60
        if latitude_dir.upper() == "S":
            latitude = -latitude
        output["latitude"] = latitude
    longitude_match = re.search(longitude_pattern, data)
    if longitude_match:
        longitude_degrees = float(longitude_match.group(1))
        longitude_minutes = float(longitude_match.group(2))
        longitude_dir = longitude_match.group(3)
        longitude = longitude_degrees + longitude_minutes / 60
        if longitude_dir.upper() == "W":
            longitude = -longitude
        output["longitude"] = longitude
        
    time_match = re.search(time_pattern, data)
    date_match = re.search(date_pattern, data)
    if date_match:
        month = int(date_match.group(1))
        day = int(date_match.group(2))
        year = int(date_match.group(3))
        timestamp = datetime(year, month, day)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))
            timestamp = datetime(year, month, day, hour, minute)
        output["date"] = timestamp.isoformat()
    wind_match = re.search(wind_pattern, data)
    if wind_match:
        output["wind_direction"] = wind_match.group(1)
        output["wind_direction_deg"] = int(wind_match.group(2))
        output["wind_speed"] = float(wind_match.group(3))
    pressure_match = re.search(pressure_pattern, data)
    if pressure_match:
        output["pressure"] = float(pressure_match.group(1))
        output["pressure_tendency"] = pressure_match.group(2)
    air_temp_match = re.search(air_temp_pattern, data)
    if air_temp_match:
        air_temp_f = float(air_temp_match.group(1))
        output["air_temp_c"] = (air_temp_f - 32) * 5 / 9
    water_temp_match = re.search(water_temp_pattern, data)
    if water_temp_match:
        water_temp_f = float(water_temp_match.group(1))
        output["water_temp_c"] = (water_temp_f - 32) * 5 / 9
    return output
