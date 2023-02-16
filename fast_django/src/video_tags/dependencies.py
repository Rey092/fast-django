from async_lru import alru_cache

from src.video_tags.manager import VideoTagManager
from src.video_tags.models import VideoTag


@alru_cache(maxsize=1)
async def get_video_tag_manager():
    return VideoTagManager(model=VideoTag)
