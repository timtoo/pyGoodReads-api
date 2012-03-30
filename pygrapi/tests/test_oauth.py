import pygrapi_test_setup

from pygrapi import oauth

import unittest

class OAuthTest(unittest.TestCase):
    def test_01(self):
        """Create objects"""
        o = oauth.OAuth()
        o = oauth.OAuth(None)
        o = oauth.OAuth('test')
        o = oauth.OAuth(token='token', secret='secret')

    def test_02(self):
        self.assertRaises(ValueError, oauth.OAuth().client)

        # need both token and secret
        self.assertRaises(ValueError, oauth.OAuth(token='token').client)
        oauth.OAuth(token='token', secret='secret').client()


