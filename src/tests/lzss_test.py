import unittest
from lzss import lzss_encode, lzss_decode

class TestLZSSFunctionality(unittest.TestCase):
    def test_simple_encode(self):
        test_string = "test in testing new string"
        result_string = "test in <8,4><7,2>g new <10,2>r<11,3>"
        self.assertEqual(lzss_encode(test_string), result_string)

    def test_buffer_size_affects_output(self):
        test_string = "test test golden retilou test"
        self.assertNotEqual(lzss_encode(test_string, 50), lzss_encode(test_string, 5))

    def test_simple_decode(self):
        test_string = "testing a <10,4>er"
        result_string = "testing a tester"
        self.assertEqual(lzss_decode(test_string), result_string)

    def test_simple_encode_decode(self):
        test_string = "testing a testy tester in a tester network of testers"
        self.assertEqual(lzss_decode(lzss_encode(test_string)), test_string)


if __name__ == '__main__':
    unittest.main()