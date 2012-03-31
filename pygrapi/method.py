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

class Base(object):
    url = ''
    method = GET
    params = {}

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

    def __call__(self, oauth_client, **kw):
        if kw:
            self.update(kw, clean=True)

        # API policy is no more than one call per
        while self.lastcall + 1 > time.time():
            time.sleep(1)

        request = self.prepare()
        logging.debug('Request: %r', request)
        response, content = oauth_client.request(*request)
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


class AuthUser(Base):
    url = 'api/auth_user'
    tag = 'user'
    oauth = True


class AuthorBooks(Base):
    url = 'author/list.xml'
    param = {
            'key': '*Developer key',
            'id': '*Goodreads author id',
            'page': 'page'
    }

class AuthorShow(Base):
    url = 'author/show.xml'
    param = {
            'key': '*Developer key',
            'id': '*Goodreads author id',
    }

class BookIsbn_to_id(Base):
    url = 'book/isbn_to_id'
    param = {
            'key': '*Developer key',
            'isbn': '*ISBN of book to lookup',
    }

class BookReview_counts(Base):
    url = 'book/review_counts.json'
    param = {
            'key': '*Developer key',
            'isbns': '*Array of ISBNs or a comma separated string of ISBNs (1000 max)',
            'format': 'json',
            'callback': 'function to wrap JSON response',
    }

class BookShow(Base):
    url = 'book/show?format=json'
    param =  {
            'rating': 'Show only reviews with a particular rating',
            'key': '*Developer key',
            'text_only': 'Only show reviews that have text (default: false)',
            'id': '*Goodreads internal book id',
            }




class AddQuote(Base):
    url = 'quotes.xml'
    method = POST
    params = {
            'body': '*The quote!',
            'author_name': '*Name of the quote author',
            'isbn': 'ISBN of the book from which the quote was taken. This will not override the book_id if it was provided',
            'book_id': 'id of the book from which the quote was taken',
            'author_id': 'id of the author',
            'tags': 'Comma-separated tags',
    }


