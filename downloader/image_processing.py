import io

from PIL import Image, ImageFilter
from rembg import remove

from exceptions import BackgroundRemovalError, ConversionError


def image_to_byte_array(image: Image) -> bytes:
    """Converts an image to a byte array in its current format."""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    return img_byte_arr.getvalue()


def adjust_images_to_resolution(image: Image, target_resolution: tuple[int, int]) -> Image:
    """Resizes an image to the target resolution with a blurred background."""
    image.thumbnail(target_resolution, Image.LANCZOS)
    background = Image.new("RGB", target_resolution, (0, 0, 0))
    bg_blur = image.resize(target_resolution, Image.LANCZOS).filter(ImageFilter.GaussianBlur(15))
    background.paste(bg_blur)
    offset = ((target_resolution[0] - image.size[0]) // 2,
              (target_resolution[1] - image.size[1]) // 2)
    background.paste(image, offset)
    return background


def remove_background(image: Image) -> Image:
    """Removes the background from an image."""
    try:
        return remove(image)
    except Exception as e:
        raise BackgroundRemovalError(f"Error removing background: {e}")


def process_image(image_path: str, resolution: tuple[int, int] = None, remove_bg: bool = False) -> None:
    """
    Processes an image with optional resizing and background removal.

    Parameters
    ----------
    image_path : str
        Path to the image to be processed.
    resolution : tuple, optional
        Target resolution for resizing, by default None.
    remove_bg : bool, optional
        If True, removes the background from the image, by default False.

    Raises
    ------
    ResolutionError, BackgroundRemovalError
        Raises specific errors depending on the processing step.
    """
    try:
        with Image.open(image_path) as img:
            if resolution:
                img = adjust_images_to_resolution(img, resolution)
            if remove_bg:
                img = remove_background(img)

            img.save(image_path)
    except Exception as e:
        raise ConversionError(f"Error processing image {image_path}: {e}")
