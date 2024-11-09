import os

from downloader.bing_downloader import BingImageDownloader
from downloader.image_processing import process_image


def get_images(search_term: str, num_images: int, output_dir: str,
               resolution: tuple[int, int] = (1080, 1920),
               remove_background: bool = False,
               img_format: str = 'PNG') -> None:
    """
    Downloads and processes images based on a specified search term.

    This function searches for images on Bing, downloads the requested quantity,
    and applies optional processing steps like resizing and background removal.
    The processed images are saved in the specified output directory.

    Parameters
    ----------
    search_term : str
        Search term to download images from Bing.
    num_images : int
        Number of images to download.
    output_dir : str
        Directory where the downloaded images will be saved.
    resolution : tuple[int, int], optional
        Target size to adjust the resolution of images (width, height).
        Defaults to (1080, 1920).
    remove_background : bool, optional
        If True, removes the background from downloaded images.
        Defaults to False.
    img_format : str, optional
        Format to save the images, must be 'PNG', 'WEBP', or 'JPEG'.
        Defaults to 'PNG'.

    Raises
    ------
    DownloadError
        If an error occurs during image download.
    ResolutionError
        If an error occurs during resolution adjustment.
    BackgroundRemovalError
        If an error occurs during background removal.
    ConversionError
        If an error occurs during image format conversion.

    Examples
    --------
    >>> get_images("Landscape", 5, "./images", resolution=(1080, 1920), remove_background=True, img_format='WEBP')
    """
    image_downloader = BingImageDownloader(search_term, num_images, output_dir)
    image_downloader.run(img_format=img_format)

    for image_name in os.listdir(output_dir):
        image_path = os.path.join(output_dir, image_name)
        process_image(image_path, resolution=resolution, remove_bg=remove_background)
