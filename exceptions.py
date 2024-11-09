class DownloadError(Exception):
    """Error raised when an image download fails."""
    pass


class ResolutionError(Exception):
    """Error raised when image resolution adjustment fails."""
    pass


class BackgroundRemovalError(Exception):
    """Error raised when background removal fails."""
    pass


class ConversionError(Exception):
    """Raised when an error occurs during image format conversion."""
    pass
