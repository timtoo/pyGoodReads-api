"""
The Base class contains most/all the methods/logic for communicating with GoodReads.

A minimal subclass is made for each API command.

The subclass names are a morphed version of the GoodReads API name. The period is
removed and the segements are camel-cased. There is a .name() method to convert
the class name back to the official GoodReads name if needed.
"""

import urllib, time
import logging
import re

from xml.etree import ElementTree

from config import config
POST = 'POST'
GET = 'GET'
PUT = 'PUT'

RAW = 'raw'
XML = 'xml'
JSON = 'json'

class Base(object):
    url = ''
    method = GET
    params = {}
    format = RAW

    def __init__(self, **kw):
        """The first argument is the optional oauth client instance.
        After that any keywords passed in will be set as command parameters.
        """
        self.data = {}
        self.update(kw)
        self.lastcall = 0

    def update(self, dct, clean=False):
        """Update object's data from dictionary"""
        if clean:
            self.data = {}
        for k in dct.keys():
            self.__setitem__(k, dct[k])
        return self

    def __setitem__(self, key, val):
        if not self.params.has_key(key):
            raise KeyError("Can not set key '%s'" % key)
        self.data[key] = val

    def __getitem__(self, key):
        if not self.params.has_key(key):
            raise KeyError("Can not get key '%s'" % key)
        return self.get(key)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def prepare(self):
        """Return dict with data prepared for communication with server"""
        url = config.url + '/' + self.url
        params = urllib.urlencode(self.data)

        if self.method == 'POST':
            result = (url, self.method, params,
                    {'content-type': 'application/x-www-form-urlencoded'})
        else:
            if params:
                if '?' in self.url:
                    url += '&'
                else:
                    url += '?'
                url += params
            result = (url, self.method)

        return result

    def name(self):
        """Convert class name to goodreads API name"""
        return re.sub(r'(\w)([A-Z])', r'\1.\2', self.__class__.__name__).lower()

    def __call__(self, client, **kw):
        if kw:
            self.update(kw, clean=True)

        # API policy is no more than one call per
        while self.lastcall + 1 > time.time():
            time.sleep(1)

        request = self.prepare()
        logging.debug('Request: %r', request)
        response, content = client.request(*request)
        logging.debug('Response: %r', response)

        if response['status'] not in ('200', '201', '202'):
            raise Exception('HTTP Error: %s' % response['status'])

        if self.tag:
            result = self.xml2dict(content, self.tag)
        else:
            result = content

        return result


    @staticmethod
    def xml2dict(xml, tag):
        tree = ElementTree.fromstring(xml)
        out = []

        for el in tree.iter(tag):
            data = { 'id' : el.get('id') }
            for tag in list(el):
                if tag.text:
                    data[tag.tag] = tag.text
            out.append(data)

        return out

