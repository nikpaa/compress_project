import unittest
from deflate import defl_encode, defl_decode


class TestDeflateFunctionality(unittest.TestCase):
    def test_simple_encode_decode(self):
        test_array = bytearray(b'deflate deflates this string accordingly if it is to be deflated.')
        self.assertEqual(defl_decode(defl_encode(test_array)), test_array)


if __name__ == '__main__':
    unittest.main()
