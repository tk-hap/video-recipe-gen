from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY
import re

formatter = TextFormatter()

# TODO: Create a video class


def validate_url(url: str) -> bool:
    # TODO: Make this logic more robust, probably needs a regex
    valid_prefixes = [
        "https://www.youtube.com/watch?v=",
        "wwww.youtube.com/watch?v=",
        "youtube.com/watch?v=",
    ]
    return any(map(url.startswith, valid_prefixes))


def validate_video_content(url: str) -> bool:
    with build("youtube", "v3", developerKey=YOUTUBE_API_KEY) as yt_service:
        request = yt_service.videos().list(part="snippet", id=url)
        response = request.execute()

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
                return True
        else:
            return False


def get_video_id(url: str) -> str:
    reg = r"^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|shorts\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*"
    video_id = re.search(reg, url).group(1)
    return video_id


def transcribe_video(video_id: str) -> str:
    video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return formatter.format_transcript(video_transcript)
