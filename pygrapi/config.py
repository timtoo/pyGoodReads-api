"""Read/provide required configuration"""

import os
import logging

logging.basicConfig(level=logging.DEBUG)

class Config(object):
    url = 'http://www.goodreads.com'

    def __init__(self, api_key=None, api_secret=None):
        self._api_key = api_key
        self._api_secret = api_secret

        if not (self._api_key or self._api_secret):
            self.load_api_keys()


    @property
    def api_key(self):
        return self._api_key

    @property
    def api_secret(self):
        return self._api_secret

    def get_oauth_token(self, userid):
        """Retrieve the oauth token for an authorized user
        (or return None)"""
        logging.error("Get Auth Token not implemented")
        return None, None

    def load_api_keys(self):
        """check various locations for API key data in a file
        (format: first line is key, second line is secret)"""
        # currently only looks for 'api.key' in this file's directory
        key_paths = [ os.path.split(__file__)[0] + os.sep + 'api.key' ]
        for p in key_paths:
            if os.path.exists(p):
                logging.info("API key file found at: %s", p)
                keys = open(p).readlines()
                if len(keys)>0:
                    self._api_key = keys[0].strip()
                if len(keys)>1:
                    self._api_secret = keys[1].strip()
                break

config = Config()

