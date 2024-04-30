import asyncio
import datetime
import logging.config
import os
import random
import uuid

import httpx

from kelp_drone.llms import (
    ChatGPT,
    Claude,
    Gemini
)

from kelp_drone.somu import SpeciesOccurrenceManagementUnit as SOMU

simulation_uuid = uuid.uuid4()

LOGGING_CONFIG = {
    "version": 1,
    "handlers": {
        "default": {
            "class": "logging.FileHandler",
            "formatter": "http",
            "filename": f"{simulation_uuid}-simulation.log"
        }
    },
    "formatters": {
        "http": {
            "format": "%(asctime)s %(levelname)s %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    'loggers': {
        'httpx': {
            'handlers': ['default'],
            'level': 'WARN',
        },
        'httpcore': {
            'handlers': ['default'],
            'level': 'WARN',
        },
        'kelp_drone.llms': {
            'handlers': ['default'],
            'level': 'INFO'
        },
        'kelp_drone.drone': {
            'handlers': ['default'],
            'level': 'INFO'
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

httpx_client = httpx.AsyncClient()

chatgpt = ChatGPT(
    name="ChatGPT 3.5",
    version="gpt-3.5-turbo",
    key=os.environ.get("OPENAI_KEY"),
    post_function=httpx_client.post
)
claude = Claude(
    name="Claude 3 Haiku",
    version="claude-3-haiku-20240307",
    key=os.environ.get("ANTHROPIC_API_KEY"),
    post_function=httpx_client.post
)
gemini = Gemini(
    name="Gemini Pro",
    version="",
    key=os.environ.get("GOOGLE_GEMINI_KEY"),
    post_function=httpx_client.post
)

def add_drone_somus(drone, number=3):
    """Adds Species Occurrence Management Units to a Drone"""
    for i in range(1, number+1):
        somu = SOMU(name=f"{drone.name} {i}")
        drone.add_somu(somu)

