from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

formatter = TextFormatter()


def validate_video(url: str) -> bool:
    # TODO: Make this logic more robust, probably needs a regex
    print(url)
    valid_prefixes = [
        "https://youtube.com/watch?v=",
        "youtube.com/watch?v=",
        "youtube.com/watch?v=",
    ]
    return all(map(url.startswith, valid_prefixes))


def get_video_id(url: str) -> str:
    video_url_list = url.split("=", maxsplit=1)
    return video_url_list[1]


def transcribe_video(video_id: str) -> str:
    if video_id == "Invalid YouTube URL":
        return video_id
    else:
        video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text_formatted = formatter.format_transcript(video_transcript)
        return text_formatted
