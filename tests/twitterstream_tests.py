import unittest
import sys
sys.path.append('../london')
from zeitgeist import twitterstream


class TwitterStreamTests(unittest.TestCase):

    lines = []

    def setUp(self):
        with open('test_records.txt') as f:
            self.lines = f.readlines()

    def test_parse_record(self):
        self.assertEquals(len(self.lines),2)
        self.assertEquals(twitterstream.parse_record(self.lines[0]),None)


    if __name__ == '__main__':
        unittest.main()