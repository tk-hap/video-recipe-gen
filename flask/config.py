import os

# Get env variables
REDIS_HOST = os.environ.get("REDISHOST", "localhost")
REDIS_PORT = int(os.environ.get("REDISPORT", 6379))
REQUEST_LIMIT = int(os.environ.get("REQUEST_LIMIT", 3))
REQUEST_TIMEOUT_SECS = int(os.environ.get("REQUEST_TIMEOUT_SECS", 60))
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
