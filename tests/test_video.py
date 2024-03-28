import pytest
import sys

sys.path.insert(0, './flask')
import video


def test_get_video_id():
    valid_urls = {
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ": "dQw4w9WgXcQ",
        "https://youtu.be/6tvBVCm9lmg?si=VuQYxsVc6tvA26KH": "6tvBVCm9lmg",
        "m.youtube.com/watch?v=S_7SE_Uzk-I": "S_7SE_Uzk-I",
        "youtube.com/watch?v=vYu4Zu5Ra_k": "vYu4Zu5Ra_k"
    }
    invalid_urls = [
        "this is a url",
        "https://www.reddit.com/"
    ]

    for url, id in valid_urls.items():
        assert video.get_video_id(url) == id
    for url in invalid_urls:
        assert video.get_video_id(url) == False

def test_validate_video_content():
    # Cooking vid id
    assert video.validate_video_content("CyGelCPUMc0") == True
    # Music vid id
    assert video.validate_video_content("dQw4w9WgXcQ") == False