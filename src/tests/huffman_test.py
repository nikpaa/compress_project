import unittest
from huffman import huff_encode, huff_decode

class TestHuffFunctionality(unittest.TestCase):
    def test_simple_encode(self):
        test_string = "aaaaaaaabbbbbbbccccd"
        result_string = "a:0 d:100 c:101 b:11 | 0000000011111111111111101101101101100"
        self.assertEqual(huff_encode(test_string), result_string)

    def test_simple_decode(self):
        test_string = "a:0 d:100 c:101 b:11 | 0000000011111111111111101101101101100"
        result_string = "aaaaaaaabbbbbbbccccd"
        self.assertEqual(huff_decode(test_string), result_string)

    def test_simple_encode_decode(self):
        test_string = "testing a testy tester in a tester network of testers"
        self.assertEqual(huff_decode(huff_encode(test_string)), test_string)


if __name__ == '__main__':
    unittest.main()



#print(test_string)
#print(lzss_encode(test_string))
#print(lzss_decode(lzss_encode(test_string)))