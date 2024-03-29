from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, MAX_VIDEO_LENGTH
from isodate import parse_duration
import re
import structlog

logger = structlog.get_logger()

formatter = TextFormatter()

# TODO: Create a video class


def get_video_id(url: str) -> str:
    reg = r"^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|shorts\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*"
    video_id = re.search(reg, url)
    if video_id is None:
        logger.info("Invalid youtube url", video_url=url)
        return False

    return video_id.group(1)


def validate_video_content(url: str) -> bool:
    with build("youtube", "v3", developerKey=YOUTUBE_API_KEY) as yt_service:
        request = yt_service.videos().list(part="snippet,contentDetails", id=url)
        response = request.execute()

        try:
            duration = response["items"][0]["contentDetails"]["duration"]
        except IndexError:
            logger.warning("Can't get video duration", yt_response=response)
            return False

        if parse_duration(duration) > parse_duration(MAX_VIDEO_LENGTH):
            logger.info(
                "Video duration too long",
                video_duration=duration,
                max_duration=MAX_VIDEO_LENGTH,
            )
            return False

        title = response["items"][0]["snippet"]["title"]
        description = response["items"][0]["snippet"]["description"]
        tags = []
        tags.append(response["items"][0]["snippet"].get("tags"))
        cooking_keywords = ["cook", "cooking", "recipe", "food", "bake", "baking"]
        for keyword in cooking_keywords:
            if (
                keyword in title.lower()
                or keyword in description.lower()
                or keyword in tags
            ):
                logger.info("Cooking tags found", video_tags=tags, video_url=url)
                return True
        else:
            logger.info("No cooking tags found", video_tags=tags, video_url=url)
            return False


def transcribe_video(video_id: str) -> str:
    video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return formatter.format_transcript(video_transcript)
