from constant import PAYMENT_PLATFORMS
from google.google_server_notification import GoogleServer
from apple.apple_server_notification import AppleServer
from roku.roku_server_notification import RokuServer


class Build:
    """
    This Class build and return payment object
    """
    payment_server_object = None

    def __init__(self, payment_platform):
        self._payment_platform = payment_platform

    def create_object(self):
        if not (self._payment_platform in PAYMENT_PLATFORMS):
            return self.payment_server_object
        if self._payment_platform == "google":
            self.payment_server_object = GoogleServer()
            return self.payment_server_object
        if self._payment_platform == "apple":
            self.payment_server_object = AppleServer()
            return self.payment_server_object
        if self._payment_platform == "roku":
            self.payment_server_object = RokuServer()
            return self.payment_server_object
