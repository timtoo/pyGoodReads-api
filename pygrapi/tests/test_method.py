import unittest

import pygrapi_test_setup
from pygrapi import method

class MethodTest(unittest.TestCase):
    def test_base(self):
        test = method.Base()

    def test_custom(self):
        class TestMethod(method.Base):
            url = 'test/method.xml'
            method = method.POST
            params = {
                    'test': 'a test method',
                    'param': 'another parameter',
                    }

        test = TestMethod()
        data = test.prepare()
        self.assertEqual(data,
                ('http://www.goodreads.com/test/method.xml',
                'POST', '',
                {'content-type': 'application/x-www-form-urlencoded'}))

        with self.assertRaises(KeyError):
            test['x']

        # values for param keys not set return None
        self.assertEqual(test['test'], None)

        test['test'] = 1
        self.assertEqual(test['test'], 1)

        test['param'] = 'test'
        data = test.prepare()
        self.assertEqual(data[2], 'test=1&param=test')

        test.method = method.GET
        data = test.prepare()
        self.assertEqual(len(data),2)
        self.assertEqual(data[0], 'http://www.goodreads.com/test/method.xml?test=1&param=test')

        test.url = 'test?method=xml'
        data = test.prepare()
        self.assertEqual(data[0], 'http://www.goodreads.com/test?method=xml&test=1&param=test')

        # make sure ? isn't added to end with empty parameter data
        test.url = 'test/method.xml'
        test.data = {}
        data = test.prepare()
        self.assertEqual(data[0], 'http://www.goodreads.com/test/method.xml')








