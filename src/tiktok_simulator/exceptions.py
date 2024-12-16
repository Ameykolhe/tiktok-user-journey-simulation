class ScraperException(Exception):
    """Exception class for scraping errors"""

    def __init__(self, message="A scraping error occurred", url=None):
        self.message = message
        self.url = url
        super().__init__(self.message)

    def __str__(self):
        error_msg = self.message
        if self.url:
            error_msg += f" | URL: {self.url}"
        return error_msg


class MaxRetryException(Exception):
    """Exception class for Max Retry Count reached"""

    def __init__(self, message="Maximum Retry Count Reached", url=None):
        self.message = message
        self.url = url
        super().__init__(self.message)

    def __str__(self):
        error_msg = self.message
        if self.url:
            error_msg += f" | URL: {self.url}"
        return error_msg
