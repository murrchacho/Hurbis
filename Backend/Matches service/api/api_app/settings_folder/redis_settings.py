import os



REDIS_HOST = os.environ.get("REDIS_HOST")

REDIS_PORT = os.environ.get("REDIS_PORT")

REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

REDIS_LINK = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"