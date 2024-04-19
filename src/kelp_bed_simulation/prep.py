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
