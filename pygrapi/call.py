
POST = 'POST'
GET = 'GET'
PUT = 'PUT'

class Base(object):
    url = ''
    method = None
    params = {}

    def __init__(self):
        self.data = {}

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

    def url(self):
        """Construct URL for this object"""
        out = self.url


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


