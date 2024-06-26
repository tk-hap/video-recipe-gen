import os
import logging
import structlog

# Get env variables
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REQUEST_LIMIT = int(os.environ.get("REQUEST_LIMIT", 3))
REQUEST_TIMEOUT_SECS = int(os.environ.get("REQUEST_TIMEOUT_SECS", 60))
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
MAX_VIDEO_LENGTH = os.environ.get("MAX_VIDEO_LENGTH", "PT45M")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# Configure structured logging
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, LOG_LEVEL)),
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)
logger = structlog.get_logger()

logger.info("Logger started")
