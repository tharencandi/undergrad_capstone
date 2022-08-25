DEFAULT_REASON = "Unknown reason for download error."


class DownloadError(Exception):
    def __init__(self, reason=DEFAULT_REASON, message=""):
        self.reason = reason
        if not message:
            super().__init__(reason)
        else:
            super().__init__(message)
