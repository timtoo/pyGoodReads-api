"""Provide OAuth services for Goodread

Originally based on example: https://gist.github.com/537923
"""

import logging

import oauth2 as oauth
import urlparse
import time

from config import config

request_token_url = '%s/oauth/request_token/' % config.url
authorize_url = '%s/oauth/authorize/' % config.url
access_token_url = '%s/oauth/access_token/' % config.url


class OAuth(object):
    def __init__(self, userid=None, token=None, secret=None):
        """Create Oauth object with userid for how user will be identified by this software"""
        self.userid = userid
        self.consumer = oauth.Consumer(key=config.api_key, secret=config.api_secret)
        self.secret = secret
        self.token = token
        self.last_client_time = 0   # for rate limiting?

    def load_token(self):
        """Return the access token for this user, or None if user has no access token"""
        if not (self.token and self.secret):
            self.token, self.secret = config.get_oauth_token(self.userid)

        token = oauth.Token(self.token, self.secret)
        return token

    def store_token(self):
        """Store the access token for this user for future use"""
        logging.debug("OAuth Access Token: %s", request)
        raise Exception('Token storage not implemented')
        return self

    def make_request(self):
        """Return dictionary with following keys:

            - oauth_token
            - oauth_token_secret
            - oauth_request_link

            This is the first step in creating an access token. Use the
            data generated here to send the user to goodreads to authorize
            our request, and then retrieve the access token via
            accepted_request()
        """
        client = oauth.Client(self.consumer)
        response, content = client.request(request_token_url, 'GET')
        if response['status'] != '200':
            raise Exception('Invalid response: %s' % response['status'])

        request = dict(urlparse.parse_qsl(content))

        request['oauth_request_link'] = '%s?oauth_token=%s' % (authorize_url,
                                                request['oauth_token'])

        logging.debug("OAuth Request: %s", request)
        return request

    def accepted_request(self, request):
        """Use the request information to get user access token"""
        token = oauth.Token(request['oauth_token'],
                    request['oauth_token_secret'])

        client = oauth.Client(self.consumer, token)
        response, content = client.request(access_token_url, 'POST')
        if response['status'] != '200':
            raise Exception('Invalid response: %s' % response['status'])

        access_token = dict(urlparse.parse_qsl(content))

            # this is the token you should save for future uses
        self.token = access_token['oauth_token']
        self.secret = access_token['oauth_token_secret']

        self.store_token()

        return self

    def client(self):
        token = self.load_token()
        client = oauth.Client(self.consumer, token)
        self.last_client_time = time.time()
        return client






