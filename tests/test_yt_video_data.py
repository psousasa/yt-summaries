import pytest
from yt_info.yt_video_data import Video, get_channel_videos, get_video_transcript


# Mocked data for tests
mock_video_data = {
    "snippet": {
        "title": "Test Video",
        "description": "Test Description",
    },
    "id": {
        "videoId": "test_video_id",
    },
}

mock_transcript_data = [
    {"text": "This is a test transcript line 1", "start": 0.0, "duration": 4.0},
    {"text": "This is a test transcript line 2", "start": 4.0, "duration": 5.0},
]


# Test Video class
def test_video_url():
    video = Video(
        title="Test Video",
        video_id="test_id",
        description="Test description",
        is_short=False,
    )
    assert video.url == "https://www.youtube.com/watch?v=test_id"

    # test raise Exception with any required field missing (all fields required)
    with pytest.raises(TypeError):
        video = Video()


# Test get_transcript function
def test_get_video_transcript(mocker):
    from youtube_transcript_api import YouTubeTranscriptApi

    mock_yt_transcript = mocker.patch("yt_info.yt_video_data.YouTubeTranscriptApi")

    mocked_response = ["this", "is", "a", "mocked", "response"]

    mock_yt_transcript.get_transcript.return_value = mocked_response

    video = Video(
        title="Test Video",
        video_id="test_id",
        description="Test description",
        is_short=False,
    )
    transcript = get_video_transcript(video)
    assert transcript == mocked_response

    # checking that any other value raises an exception
    with pytest.raises(Exception):
        transcript = get_video_transcript("video")


# test_my_youtube_module.py
import pytest


def test_get_channel_videos(mocker):
    # Step 1: Mock the build function
    mock_build = mocker.patch("yt_info.yt_video_data.build")

    # Step 2: Create a mock YouTube service object
    mock_youtube = mocker.Mock()
    mock_build.return_value = mock_youtube

    # Step 3: Mock the search().list().execute() chain
    mock_search = mock_youtube.search.return_value
    mock_list = mock_search.list.return_value

    # Mock the response for the first page of results
    mock_list.execute.return_value = {
        "kind": "youtube#searchListResponse",
        "etag": "ZjR2tYfEN5h6JgAdMI-EAH8H2iE",
        "nextPageToken": None,
        "regionCode": "PT",
        "pageInfo": {"totalResults": 61663, "resultsPerPage": 50},
        "items": [
            {
                "kind": "youtube#searchResult",
                "etag": "KLCzPk0LeHDcFT3S0UssTCBcEMA",
                "id": {"kind": "youtube#video", "videoId": "heRFk1cmGA0"},
                "snippet": {
                    "publishedAt": "2024-06-18T15:00:41Z",
                    "channelId": "UChBEbMKI1eCcejTtmI32UEw",
                    "title": "4 Ways To Use Garlic",
                    "description": "",
                    "thumbnails": {
                        "default": {
                            "url": "https://i.ytimg.com/vi/heRFk1cmGA0/default.jpg",
                            "width": 120,
                            "height": 90,
                        },
                        "medium": {
                            "url": "https://i.ytimg.com/vi/heRFk1cmGA0/mqdefault.jpg",
                            "width": 320,
                            "height": 180,
                        },
                        "maxres": {
                            "url": "https://i.ytimg.com/vi/heRFk1cmGA0/hqdefault.jpg",
                            "width": 480,
                            "height": 360,
                        },
                    },
                    "channelTitle": "Joshua Weissman",
                    "liveBroadcastContent": "none",
                    "publishTime": "2024-06-18T15:00:41Z",
                },
            },
            {
                "kind": "youtube#searchResult",
                "etag": "WOyT9_px2gfsnOJxN6y2-u1kWHY",
                "id": {"kind": "youtube#video", "videoId": "YfS_dOOiong"},
                "snippet": {
                    "publishedAt": "2024-03-07T20:35:00Z",
                    "channelId": "UChBEbMKI1eCcejTtmI32UEw",
                    "title": "The BEST Caesar Salad Ever",
                    "description": "A description for the BEST Caesar Salad",
                    "thumbnails": {
                        "default": {
                            "url": "https://i.ytimg.com/vi/YfS_dOOiong/default.jpg",
                            "width": 120,
                            "height": 90,
                        },
                        "medium": {
                            "url": "https://i.ytimg.com/vi/YfS_dOOiong/mqdefault.jpg",
                            "width": 320,
                            "height": 180,
                        },
                        "high": {
                            "url": "https://i.ytimg.com/vi/YfS_dOOiong/hqdefault.jpg",
                            "width": 480,
                            "height": 360,
                        },
                    },
                    "channelTitle": "Joshua Weissman",
                    "liveBroadcastContent": "none",
                    "publishTime": "2024-03-07T20:35:00Z",
                },
            },
        ],
    }

    # Step 4: Call the function under test
    api_key = "fake_api_key"
    channel_id = "fake_channel_id"
    result = get_channel_videos(channel_id, api_key)

    # Step 5: Assertions
    mock_build.assert_called_once_with("youtube", "v3", developerKey=api_key)
    mock_youtube.search.assert_called_once()
    mock_search.list.assert_called_once_with(
        part="snippet",
        channelId=channel_id,
        maxResults=50,
        type="video",
        pageToken=None,
    )
    mock_list.execute.assert_called_once()

    # Ensure the function returns the expected data
    assert len(result) == 2
    assert result[0].title == "4 Ways To Use Garlic"
    assert result[0].video_id == "heRFk1cmGA0"
    assert result[0].description == ""
    assert not result[0].is_short  # Assuming "maxres" was in the snippet
    assert result[1].title == "The BEST Caesar Salad Ever"
    assert result[1].video_id == "YfS_dOOiong"
    assert result[1].description == "A description for the BEST Caesar Salad"
    assert result[1].is_short
