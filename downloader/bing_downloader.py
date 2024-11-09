import io
import re
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

from config.settings import (
    USER_AGENT_HEADERS, IMAGE_FILTERS, BING_ADULT_FILTER,
    REQUEST_TIMEOUT, BING_IMAGE_SEARCH_URL, BING_IMAGE_SEARCH_PARAMS_TEMPLATE
)
from downloader.utils import generate_uuid_2
from exceptions import DownloadError


class BingImageDownloader:
    """
    Searches and downloads images from Bing to a specified directory.
    """

    def __init__(self, query: str, image_limit: int, save_directory: str) -> None:
        """
        Initializes search parameters and download settings.
        """
        self.query = query
        self.image_limit = image_limit
        self.save_directory = Path(save_directory)
        self.adult_filter = BING_ADULT_FILTER
        self.timeout = REQUEST_TIMEOUT
        self.image_filter = ''
        self.images_downloaded = 0
        self.page_number = 0
        self.downloaded_urls = set()
        self.headers = USER_AGENT_HEADERS

    @staticmethod
    def map_image_filter(shorthand: str) -> str:
        """
        Maps shorthand filter names to Bing-compatible filter strings.
        """
        return IMAGE_FILTERS.get(shorthand, "")

    def save_image(self, link: str, file_path: Path, img_format: str) -> None:
        """
        Downloads an image from a URL and saves it to a file.
        """
        try:
            request = urllib.request.Request(link, None, self.headers)
            image_data = urllib.request.urlopen(request, timeout=self.timeout).read()
            with Image.open(io.BytesIO(image_data)) as img:
                if img_format == "png" and img.mode != "RGBA":
                    img = img.convert("RGBA")
                elif img_format in {"webp", "jpeg"} and img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(file_path, format=img_format.upper())
        except Exception as e:
            raise DownloadError(f"Failed to save image from {link} to {file_path} in format {img_format}: {e}")

    def download_image(self, link: str, img_format: str = 'PNG') -> None:
        """
        Saves a validated image from a URL link.
        """
        valid_formats = {"png", "webp", "jpeg"}
        img_format = img_format.lower() if img_format.lower() in valid_formats else "png"

        file_name = f"{generate_uuid_2()}_{self.images_downloaded}.{img_format}"
        file_path = self.save_directory / file_name

        try:
            self.save_image(link, file_path, img_format)
        except Exception as e:
            raise DownloadError(f"Error downloading and saving image from {link}: {e}")

    def run(self, img_format: str = 'PNG') -> None:
        """
        Executes the image search and download process.
        """
        while self.images_downloaded < self.image_limit:
            request_url = (
                    f'{BING_IMAGE_SEARCH_URL}{urllib.parse.quote_plus(self.query)}'
                    + BING_IMAGE_SEARCH_PARAMS_TEMPLATE.format(page_counter=self.page_number,
                                                               limit=self.image_limit,
                                                               adult=self.adult_filter,
                                                               filter=self.map_image_filter(self.image_filter)
                                                               )
            )
            try:
                request = urllib.request.Request(request_url, None, self.headers)
                response = urllib.request.urlopen(request)
                html = response.read().decode('utf8')
                links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

                for link in links:
                    if link not in self.downloaded_urls and self.images_downloaded < self.image_limit:
                        self.downloaded_urls.add(link)
                        self.images_downloaded += 1
                        self.download_image(link, img_format=img_format)

                if not links:
                    break

                self.page_number += 1
            except Exception as e:
                raise DownloadError(f"Error during search execution: {e}")
