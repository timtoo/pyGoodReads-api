"""Goodreads API methods"""

from base import Base
from base import POST, GET, PUT
from base import RAW, XML, JSON

class AuthUser(Base):
    url = 'api/auth_user'
    tag = 'user'
    oauth = True
    format = RAW


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
    url = 'book/show'
    param =  {
            'rating': 'Show only reviews with a particular rating',
            'key': '*Developer key',
            'text_only': 'Only show reviews that have text (default: false)',
            'id': '*Goodreads internal book id',
            'format': 'xml or json',
            }

class BookShow_by_isbn(Base):
    url = 'book/show'
    param =  {
            'rating': 'Show only reviews with a particular rating',
            'key': '*Developer key',
            'isbn': '*The ISBN of the book to look up',
            'user_id': '*3882378 (required only for JSON)',
            'callback': 'function ot wrap JSON response if format=json',
            'format': 'xml or json',
            }


class Owned_booksList(Base):
    url = 'owned_books/user?format=xml'
    param = {
        'page': '1-N (optional, default 1)',
        'id': 'Goodreads user_id',
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


