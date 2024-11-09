# Image Downloader

This library provides a streamlined way to download and process images based on a specified search term using Bing's image search. The main function, `get_images`, allows users to download images with options for resizing, background removal, and format conversion.

## Installation

WIP pip

## Usage

The main function of this library is `get_images`, which downloads and processes images based on your parameters. This function is located in the main script and provides flexible options for image processing.

### Get Images

```python
def get_images(search_term: str, num_images: int, output_dir: str,
               resolution: tuple[int, int] = (1080, 1920),
               remove_background: bool = False,
               img_format: str = 'PNG') -> None:
```

### Parameters

- **`search_term`** (`str`): The search term for downloading images from Bing.
- **`num_images`** (`int`): Number of images to download.
- **`output_dir`** (`str`): Directory path where the images will be saved.
- **`resolution`** (`tuple[int, int]`, optional): Target resolution for resizing the images. Defaults to `(1080, 1920)`.
- **`remove_background`** (`bool`, optional): If `True`, removes the background from each downloaded image. Defaults to `False`.
- **`img_format`** (`str`, optional): Image format for saving images. Must be one of `'PNG'`, `'WEBP'`, or `'JPEG'`. Defaults to `'PNG'`.

### Exceptions

- **`DownloadError`**: Raised if an error occurs during image download.
- **`ResolutionError`**: Raised if an error occurs during image resizing.
- **`BackgroundRemovalError`**: Raised if an error occurs while removing the background from an image.
- **`ConversionError`**: Raised if an error occurs during image format conversion.

### Example Usage

```python
from image_downloader import get_images

# Download and process images based on a search term
get_images(
    search_term="Landscape",
    num_images=5,
    output_dir="./images",
    resolution=(1080, 1920),
    remove_background=True,
    img_format="WEBP"
)
```

In this example, the function downloads 5 images related to "Landscape," saves them in `WEBP` format, resizes them to `1080x1920` resolution, and removes their backgrounds.


## License

This project is licensed under the MIT License. See the LICENSE file for more details.
