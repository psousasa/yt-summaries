from dataclasses import dataclass
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi


@dataclass(slots=False)
class Video:
    title: str
    video_id: str
    description: str
    is_short: bool

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"


def get_channel_videos(channel_id, api_key) -> list[Video]:
    """_summary_

        Parameters
        ----------
        channel_id : _type_
            _description_
        api_key : _type_
            _description_

        Returns
        -------
        list[Video]
            Each object contains title, video_id, url
            eg. [{'title': '4 Ways To Use Garlic', 'video_id': 'heRFk1cmGA0'}
    ]
    """
    youtube = build("youtube", "v3", developerKey=api_key)

    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            type="video",
            pageToken=next_page_token,
        )
        response = request.execute()

        for item in response["items"]:

            video = Video(
                title=item["snippet"]["title"],
                video_id=item["id"]["videoId"],
                description=item["snippet"]["description"],
                is_short="maxres" not in item["snippet"],
            )
            videos.append(video)

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return videos


def get_transcript(video: Video) -> list[str]:

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video.video_id)
        return transcript
    except Exception as exception:
        raise exception
