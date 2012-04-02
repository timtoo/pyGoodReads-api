from config import config
from oauth import OAuth
import httplib2


class GoodReads(object):
    """Wrapper around config, and other objects to provide context
    for the API methods"""

    def __init__(self, oauth_token=None, oauth_token_secret=None):
        self.config = config
        self.oauth_client = None
        self.http_client = httplib2.Http()

        if (oauth_token and oauth_token_secret):
            self.oauth_client = OAuth(token=oauth_token, secret=oauth_token_secret).client()





