# -*- coding: utf-8 -*-
"""Image service."""
import io
import uuid
from math import fabs, floor
from typing import List

from django.core.files import File
from fastapi import UploadFile
from PIL import Image, ImageSequence

from src.users.api_errors import InvalidImageException


class ImageService:
    """Image service."""

    @staticmethod
    def transform_frame(frame: Image, crop_w: int, crop_h: int, img_w: int, img_h: int):
        """
        Resizes and crops the individual frame in the image.
        """
        # resize the image to the specified height if crop_w is null in the recipe
        if crop_w is None:
            if crop_h == img_h:
                return frame
            new_w = floor(img_w * crop_h / img_h)
            new_h = crop_h
            return frame.resize((new_w, new_h))

        # return the original image if crop size is equal to img size
        if crop_w == img_w and crop_h == img_h:
            return frame

        # first resize to get most visible area of the image and then crop
        w_diff = fabs(crop_w - img_w)
        h_diff = fabs(crop_h - img_h)
        enlarge_image = True if crop_w > img_w or crop_h > img_h else False
        shrink_image = True if crop_w < img_w or crop_h < img_h else False

        # define new width and height
        new_w, new_h = 0, 0

        if enlarge_image is True:
            new_w = floor(crop_h * img_w / img_h) if h_diff > w_diff else crop_w
            new_h = floor(crop_w * img_h / img_w) if h_diff < w_diff else crop_h

        if shrink_image is True:
            new_w = crop_w if h_diff > w_diff else floor(crop_h * img_w / img_h)
            new_h = crop_h if h_diff < w_diff else floor(crop_w * img_h / img_w)

        left = (new_w - crop_w) // 2
        right = left + crop_w
        top = (new_h - crop_h) // 2
        bottom = top + crop_h

        return frame.resize((new_w, new_h)).crop((left, top, right, bottom))

    def transform_image(self, original_img: Image, crop_w: int, crop_h: int):
        """
        Resizes and crops the image to the specified crop_w and crop_h if necessary.

        Works with multi frame gif and webp images also.

        args:
        original_img is the image instance created by pillow ( Image.open(filepath) )
        crop_w is the width in pixels for the image that will be resized and cropped
        crop_h is the height in pixels for the image that will be resized and cropped

        returns:
        Instance of an Image or list of frames which they are instances of an Image individually
        """
        img_w, img_h = (original_img.size[0], original_img.size[1])
        n_frames = getattr(original_img, "n_frames", 1)

        # single frame image
        if n_frames == 1:
            return self.transform_frame(original_img, crop_w, crop_h, img_w, img_h)
        # in the case of a multi-frame image
        else:
            frames = []
            for frame in ImageSequence.Iterator(original_img):
                frames.append(self.transform_frame(frame, crop_w, crop_h, img_w, img_h))
            return frames

    @staticmethod
    def verify_image(avatar: UploadFile) -> Image:
        """
        Verify the avatar image.
        """
        try:
            image = Image.open(avatar.file)
            image.verify()
            image = Image.open(avatar.file)
        except Exception:
            raise InvalidImageException

        return image

    def _process_image(self, media: Image, width: int, height: int) -> File:
        """
        Create an avatar from the uploaded file.
        """
        # create a buffer to store the image
        buffer = io.BytesIO()

        # check if avatar is animated
        if media.is_animated:
            # resize and crop the image
            frames: List[Image] = self.transform_image(original_img=media, crop_h=height, crop_w=width)
            frames[0].save(buffer, "WEBP", save_all=True, append_images=frames[1:])
        else:
            # resize and crop the image
            image: Image = self.transform_image(original_img=media, crop_h=height, crop_w=width)
            image.save(buffer, "WEBP")

        buffer.seek(0)

        return File(buffer, name=f"{uuid.uuid4()}.webp")
