# -*- coding: utf-8 -*-
"""MagicImageField."""
from io import BytesIO

from django.conf import settings
from django.core import checks
from django.core.files.base import ContentFile
from PIL import ExifTags, Image, ImageFile, ImageOps, ImageSequence

try:
    from sorl.thumbnail import ImageField
except ImportError:
    from django.db.models import ImageField


DEFAULT_SIZE = getattr(settings, "DJANGORESIZED_DEFAULT_SIZE", [1920, 1080])
DEFAULT_SCALE = getattr(settings, "DJANGORESIZED_DEFAULT_SCALE", None)
DEFAULT_QUALITY = getattr(settings, "DJANGORESIZED_DEFAULT_QUALITY", -1)
DEFAULT_KEEP_META = getattr(settings, "DJANGORESIZED_DEFAULT_KEEP_META", True)
DEFAULT_FORCE_FORMAT = getattr(settings, "DJANGORESIZED_DEFAULT_FORCE_FORMAT", None)
DEFAULT_FORMAT_EXTENSIONS = getattr(settings, "DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS", {})
DEFAULT_NORMALIZE_ROTATION = getattr(settings, "DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION", True)


def normalize_rotation(image):  # noqa
    """
    Find orientation header and rotate the actual data instead.

    Adapted from https://stackoverflow.com/a/6218425/723090
    """
    try:
        image._getexif()  # noqa
    except AttributeError:
        """No exit data; this image is not a jpg and can be skipped."""
        return image

    for orientation in ExifTags.TAGS.keys():
        """Look for orientation header, stop when found."""
        if ExifTags.TAGS[orientation] == "Orientation":
            break
    else:
        """No orientation header found, do nothing."""
        return image
    """ Apply the different possible orientations to the data; preserve format. """
    image_format = image.format
    exif = image._getexif()  # noqa
    if exif is None:
        return image
    action_nr = exif.get(orientation, None)
    if action_nr is None:
        """Empty orientation exif data"""
        return image
    if action_nr in (3, 4):
        image = image.rotate(180, expand=True)
    elif action_nr in (5, 6):
        image = image.rotate(270, expand=True)
    elif action_nr in (7, 8):
        image = image.rotate(90, expand=True)
    if action_nr in (2, 4, 5, 7):
        image = ImageOps.mirror(image)
    image.format = image_format
    return image


class MagicImageFieldFile(ImageField.attr_class):
    """MagicImageFieldFile."""

    rgb_formats = ("JPEG", "JPG")
    rgba_formats = ("PNG",)
    animated_formats = ("WEBP",)

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.img_format = None

    def save(self, name, content, save=True):
        """Save the image to the storage backend."""
        content.file.seek(0)
        img = Image.open(content.file)
        self.img_format = img.format if self.field.force_format is None else self.field.force_format

        if DEFAULT_NORMALIZE_ROTATION:
            img = normalize_rotation(img)  # noqa

        new_content = BytesIO()
        n_frames = getattr(img, "n_frames", 1) if img.is_animated else 1
        if n_frames == 1:
            new_content = self.resize_one_frame(img, new_content)
        else:
            new_content = self.resize_multiple_frames(img, new_content)

        new_content = ContentFile(new_content.getvalue())
        name = self.get_name(name, self.img_format)
        super(MagicImageFieldFile, self).save(name, new_content, save)

    def resize_multiple_frames(self, img: Image, new_content: BytesIO) -> BytesIO:
        """Resize multiple frames."""
        frames = []
        for frame in ImageSequence.Iterator(img):
            resized_frame = self.resize_frame(frame)
            frames.append(resized_frame)
        img = frames[0]
        self.img_format = self.animated_formats[0]
        img.save(
            new_content,
            format=self.animated_formats[0],
            quality=self.field.quality,
            save_all=True,
            append_images=frames[1:],
        )
        return new_content

    def resize_one_frame(self, img: Image, new_content: BytesIO) -> BytesIO:
        """Resize one frame."""
        thumb = self.resize_frame(img)
        thumb.save(new_content, format=self.img_format, quality=self.field.quality)
        return new_content

    def resize_frame(self, frame: Image) -> Image:
        """Resize the frame."""
        if self.field.force_format and self.field.force_format.upper() in self.rgb_formats and frame.mode != "RGB":
            frame = frame.convert("RGB")
        if self.field.force_format and self.field.force_format.upper() in self.rgba_formats and frame.mode != "RGBA":
            frame = frame.convert("RGBA")
        resample = Image.ANTIALIAS
        if self.field.size is None:
            self.field.size = frame.size
        if self.field.crop:
            thumb = ImageOps.fit(frame, self.field.size, resample, centering=self.get_centring())
        elif None in self.field.size:
            thumb = frame
            if self.field.size[0] is None and self.field.size[1] is not None:
                self.field.scale = self.field.size[1] / frame.size[1]
            elif self.field.size[1] is None and self.field.size[0] is not None:
                self.field.scale = self.field.size[0] / frame.size[0]
        else:
            frame.thumbnail(
                self.field.size,
                resample,
            )
            thumb = frame
        if self.field.scale is not None:
            thumb = ImageOps.scale(thumb, self.field.scale, resample)
        img_info = frame.info
        if not self.field.keep_meta:
            img_info.pop("exif", None)
        ImageFile.MAXBLOCK = max(ImageFile.MAXBLOCK, thumb.size[0] * thumb.size[1])
        return thumb

    @staticmethod
    def get_name(name, img_format):
        """Get the name of the image."""
        extensions = Image.registered_extensions()
        extensions = {v: k for k, v in extensions.items()}
        extensions.update(
            {
                "PNG": ".png",  # It uses .apng otherwise
            }
        )
        extensions.update(DEFAULT_FORMAT_EXTENSIONS)
        if img_format in extensions:
            name = name.rsplit(".", 1)[0] + extensions[img_format]
        return name

    def get_centring(self):
        """Get the centring for the image."""
        vertical = {
            "top": 0,
            "middle": 0.5,
            "bottom": 1,
        }
        horizontal = {
            "left": 0,
            "center": 0.5,
            "right": 1,
        }
        return [
            vertical[self.field.crop[0]],
            horizontal[self.field.crop[1]],
        ]


class MagicImageField(ImageField):
    """MagicImageField class."""

    attr_class = MagicImageFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        """Initialize the field."""
        self.size = kwargs.pop("size", DEFAULT_SIZE)
        self.scale = kwargs.pop("scale", DEFAULT_SCALE)
        self.crop = kwargs.pop("crop", None)
        self.quality = kwargs.pop("quality", DEFAULT_QUALITY)
        self.keep_meta = kwargs.pop("keep_meta", DEFAULT_KEEP_META)
        self.force_format = kwargs.pop("force_format", DEFAULT_FORCE_FORMAT)
        super(MagicImageField, self).__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        """Deconstruct the field."""
        name, path, args, kwargs = super(ImageField, self).deconstruct()
        for custom_kwargs in [
            "crop",
            "size",
            "scale",
            "quality",
            "keep_meta",
            "force_format",
        ]:
            kwargs[custom_kwargs] = getattr(self, custom_kwargs)
        return name, path, args, kwargs

    def check(self, **kwargs):
        """Run checks."""
        return [
            *super().check(**kwargs),
            *self._check_single_dimension_crop(),
            *self._check_webp_quality(),
        ]

    def _check_single_dimension_crop(self):
        """Check that the crop argument is not used with a single dimension size."""
        if self.crop is not None and self.size is not None and None in self.size:
            return [
                checks.Error(
                    f"{self.__class__.__name__} has both a crop argument and a single dimension size. "
                    "Crop is not possible in that case as the second size dimension is computed from the "
                    "image size and the image will never be cropped.",
                    obj=self,
                    id="django_resized.E100",
                    hint="Remove the crop argument.",
                )
            ]
        else:
            return []

    def _check_webp_quality(self):
        """Check that the quality argument is set when using webp."""
        if (
            self.force_format is not None
            and self.force_format.lower() == "webp"
            and (self.quality is None or self.quality == -1)
        ):
            return [
                checks.Error(
                    f"{self.__class__.__name__} forces the webp format without the quality set.",
                    obj=self,
                    id="django_resized.E101",
                    hint="Set the quality argument.",
                )
            ]
        else:
            return []
