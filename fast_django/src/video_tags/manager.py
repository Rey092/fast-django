from src.video_tags.models import VideoTag


class VideoTagManager:

    def __init__(self, model):
        self.model = model

    async def list(self):
        print([tag async for tag in self.model.objects.all()])
        return [tag async for tag in self.model.objects.all()]
