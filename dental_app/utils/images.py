"""Image helpers — circular-cropped logo loading used across views."""
import logging

from PIL import Image, ImageDraw, ImageTk

from dental_app.core.config import asset_path

log = logging.getLogger(__name__)


def load_circular_image(name: str, size: int):
    """Load an image from assets/, crop to a circle, resize to size×size.

    Returns a PhotoImage, or None if the file can't be loaded.
    """
    try:
        img = Image.open(asset_path(name))
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
        img = img.resize((size, size), Image.LANCZOS)
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)
    except Exception as err:
        log.warning("Could not load image %s: %s", name, err)
        return None


def load_image_cover(name: str, target_width: int, target_height: int):
    """Load an image resized to cover the target box (aspect preserved)."""
    try:
        img = Image.open(asset_path(name))
        aspect = img.width / img.height
        new_height = target_height
        new_width = int(new_height * aspect)
        if new_width < target_width:
            new_width = target_width
            new_height = int(new_width / aspect)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as err:
        log.warning("Could not load image %s: %s", name, err)
        return None
