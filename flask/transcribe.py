from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

formatter = TextFormatter() 

def transcribe_video(video_id: str) -> str:
    video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text_formatted = formatter.format_transcript(video_transcript)
    return text_formatted