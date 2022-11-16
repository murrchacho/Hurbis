from typing import Optional
from aiohttp import ClientSession
import redis

AIOHTTP_SESSION: Optional[ClientSession] = None
REDIS_SESSION: Optional[redis.Redis] = None