import unittest
from huffman import huff_encode, huff_decode


class TestHuffFunctionality(unittest.TestCase):
    def test_simple_encode_decode(self):
        test_array = bytearray(b'testing a testy tester in a tester network of testers')
        self.assertEqual(huff_decode(huff_encode(test_array)), test_array)


if __name__ == '__main__':
    unittest.main()
