from fastapi import APIRouter, Depends

from src.video_tags.dependencies import get_video_tag_manager
from src.video_tags.manager import VideoTagManager

tags_router = APIRouter(prefix="/tags", tags=["tags"])


@tags_router.get("/")
async def get_tags(
    video_tag_manager: VideoTagManager = Depends(get_video_tag_manager)
):
    return await video_tag_manager.list()
