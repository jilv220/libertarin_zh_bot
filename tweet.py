from dataclasses import dataclass

@dataclass
class Tweet:
    id: int
    text: str
    is_media: bool
    media_url: str