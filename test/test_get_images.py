import os
import unittest
from unittest.mock import patch, MagicMock
from exceptions import DownloadError, ResolutionError, BackgroundRemovalError, ConversionError
from scripts.main import get_images


class TestGetImages(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory for tests."""
        self.test_dir = "./test_images"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """Clean up the temporary directory after tests."""
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            os.remove(file_path)
        os.rmdir(self.test_dir)

    @patch("image_downloader.get_images.BingImageDownloader")
    @patch("image_downloader.get_images.process_image")
    def test_get_images_default(self, mock_process_image, MockBingImageDownloader):
        """Test get_images with default parameters."""
        mock_downloader = MockBingImageDownloader.return_value
        mock_downloader.run = MagicMock()

        get_images("test_search", 3, self.test_dir)

        mock_downloader.run.assert_called_once_with(img_format="PNG")
        self.assertEqual(mock_process_image.call_count, 3)

    @patch("image_downloader.get_images.BingImageDownloader")
    @patch("image_downloader.get_images.process_image")
    def test_get_images_custom_resolution_format(self, mock_process_image, MockBingImageDownloader):
        """Test get_images with custom resolution and format."""
        mock_downloader = MockBingImageDownloader.return_value
        mock_downloader.run = MagicMock()

        get_images("test_search", 3, self.test_dir, resolution=(800, 600), img_format="WEBP")

        mock_downloader.run.assert_called_once_with(img_format="WEBP")
        mock_process_image.assert_called_with(
            os.path.join(self.test_dir, 'mocked_image'),
            resolution=(800, 600),
            remove_bg=False
        )

    @patch("image_downloader.get_images.BingImageDownloader")
    @patch("image_downloader.get_images.process_image")
    def test_get_images_with_background_removal(self, mock_process_image, MockBingImageDownloader):
        """Test get_images with background removal enabled."""
        mock_downloader = MockBingImageDownloader.return_value
        mock_downloader.run = MagicMock()

        get_images("test_search", 2, self.test_dir, remove_background=True)

        mock_downloader.run.assert_called_once_with(img_format="PNG")
        mock_process_image.assert_called_with(
            os.path.join(self.test_dir, 'mocked_image'),
            resolution=(1080, 1920),
            remove_bg=True
        )

    @patch("image_downloader.get_images.BingImageDownloader")
    @patch("image_downloader.get_images.process_image")
    def test_get_images_error_handling(self, mock_process_image, MockBingImageDownloader):
        """Test get_images raises errors properly."""
        mock_downloader = MockBingImageDownloader.return_value
        mock_downloader.run.side_effect = DownloadError("Download error")

        with self.assertRaises(DownloadError):
            get_images("test_search", 2, self.test_dir)

        mock_process_image.side_effect = ResolutionError("Resolution error")

        with self.assertRaises(ResolutionError):
            get_images("test_search", 2, self.test_dir, resolution=(800, 600))

        mock_process_image.side_effect = BackgroundRemovalError("Background removal error")

        with self.assertRaises(BackgroundRemovalError):
            get_images("test_search", 2, self.test_dir, remove_background=True)

        mock_process_image.side_effect = ConversionError("Conversion error")

        with self.assertRaises(ConversionError):
            get_images("test_search", 2, self.test_dir, img_format="WEBP")

