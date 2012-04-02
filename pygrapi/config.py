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

    def find_file(self, filename, extra=(), caller_file=None):
        """Search various places for a filename and return first hit.

        Also tries filename with a dot in front of it, on each path.

        caller_file can be the filename (__file__) of the calling file,
        instead of the path of the module file.

        Optionally pass in list of extra paths to search
        """

        paths = (
                os.path.expanduser('~'),
                os.path.expanduser('~/.config'),
                os.path.expanduser('~/.local'),
                os.path.split(os.path.abspath(caller_file or __file__))[0],
                )
        if extra:
            paths = tuple(extra) + paths

        logging.debug('file_file "%s" on paths: %r', filename, paths)

        for p in paths:

            fn = os.path.join(p, filename)
            if os.path.exists(fn):
                return fn

            dotfn = os.path.join(p, '.' + filename)
            if os.path.exists(dotfn):
                return dotfn

        return None

    def load_api_keys(self):
        """check various locations for API key data in a file
        (format: first line is key, second line is secret)"""
        # currently only looks for 'api.key' in this file's directory
        key_paths = [ os.path.split(__file__)[0] + os.sep + 'api.key' ]
        fn = self.find_file('goodreads-api.key')
        if fn:
            logging.info("API key file found at: %s", fn)
            keys = open(fn).readlines()
            if len(keys)>0:
                self._api_key = keys[0].strip()
            if len(keys)>1:
                self._api_secret = keys[1].strip()

config = Config()

