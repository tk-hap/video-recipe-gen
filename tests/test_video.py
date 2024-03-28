import pytest
import sys

sys.path.insert(0, './flask')
import video


def test_validate_url():
    assert video.validate_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == True
    assert video.validate_url("not a url") == False

def test_validate_video_content():
    # Cooking vid id
    assert video.validate_video_content("CyGelCPUMc0") == True
    # Music vid id
    assert video.validate_video_content("dQw4w9WgXcQ") == False