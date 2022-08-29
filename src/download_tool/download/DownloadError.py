class DownloadError(Exception):
    DEFAULT_MSG = "Unknown reason for download error."
    def __init__(self, message):
        if not message:
            message = DownloadError.DEFAULT_MSG
        super().__init__(message)


class DownloadIntegrityError(DownloadError):
    def __init__(self):
        super().__init__("Downloaded data did not match the provided checksum.")

