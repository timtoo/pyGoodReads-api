"""Base object for representing/handling goodreads data"""

import logging
from xml.dom import minidom, Node
from xml.parsers.expat import ExpatError, ErrorString


class GoodReadsObject(object):
    """An object modelling a goodreads object. Features:

        - data accessable as a dictionary
        - parse XML from goodreads
        - create XML for goodreads?
        - serializable?

    """
    def __init__(self):
        self.data = {}

    def parseXML(self, xml):
        """Create an object FROM xml"""




