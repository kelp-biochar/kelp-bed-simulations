import asyncio
import datetime
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

