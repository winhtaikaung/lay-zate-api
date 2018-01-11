import unittest

from _blake2 import blake2b


class TestHash(unittest.TestCase):

    def test_scrapper(self):
        h = blake2b()
        h.update(u"G3215532Q".encode('utf8'))
        hash_fin = h.hexdigest()
        self.assertEqual(hash_fin, h.hexdigest())
