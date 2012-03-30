import urllib, time

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
        self.client = oauth_client
        self.update(kw)
        self.lastcall = 0

    def update(self, dct, clean=False):
        """Update object's data from dictionary"""
        if clean:
            self.data = {}
        for k in dct.keys():
            self.__setitem__(k, dct[k])

    def __setitem__(self, key, val):
        if not self.params.has_key(key):
            raise KeyError("Can not set key '%s'" % key)
        self.data[key] = str(val)

    def __getitem__(self, key):
        if not self.params.has_key(key):
            raise KeyError("Can not get key '%s'" % key)
        return self.get(key)

    def get(self, key, default=None):
        return self.data.get(key, default=default)

    def prepare(self):
        """Return dict with data prepared for communication with server"""
        url = config.url + '/' + self.url
        params = urllib.urlencode(data)

        if self.method == 'POST':
            result = (url, self.method, params,
                    {'content-type': 'application/x-www-form-urlencoded'})
        else:
            if '?' in self.url:
                url += '&'
            else:
                url += '?'
            url += parms
            result = (url, self.method)

        return result

    def __call__(oauth_client, **kw):
        if kw:
            self.update(kw, clean=True)

        # API policy is no more than one call per
        while self.lastcall + 1 > time.time():
            time.sleep(1)

        response, content = client.request(self.prepare())
        print response
        print content



class AuthUser(Base):
    url = 'api/auth_user'
    method = GET


class AuthorBooks(Base):
    url = 'author/list.xml'
    method = GET
    params = {
            'key': '*Developer key',
            'id': '*Goodreads author id',
            'page': 'page'
    }

class AuthorShow(Base):
    url = 'author/show.xml'
    method = GET
    param = {
            'key': '*Developer key',
            'id': '*Goodreads author id',
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


