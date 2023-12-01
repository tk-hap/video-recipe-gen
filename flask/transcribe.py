from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

formatter = TextFormatter() 

def get_video_id(url: str) -> str:
    video_url_list = url.split('=', maxsplit=1)
    return video_url_list[1]

def transcribe_video(video_id: str) -> str:
    if video_id == "Invalid YouTube URL":
        return video_id
    else:
        video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text_formatted = formatter.format_transcript(video_transcript)
        return text_formatted