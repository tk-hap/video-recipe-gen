import os
import logging
import structlog

# Get env variables
REDIS_HOST = os.environ.get("REDISHOST", "localhost")
REDIS_PORT = int(os.environ.get("REDISPORT", 6379))
REQUEST_LIMIT = int(os.environ.get("REQUEST_LIMIT", 3))
REQUEST_TIMEOUT_SECS = int(os.environ.get("REQUEST_TIMEOUT_SECS", 60))
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
MAX_VIDEO_LENGTH = os.environ.get("MAX_VIDEO_LENGTH", "PT45M")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

# Configure structured logging
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, LOG_LEVEL))
)
logger = structlog.get_logger()

