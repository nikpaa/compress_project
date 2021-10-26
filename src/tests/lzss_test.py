import unittest
from lzss import lzss_encode, lzss_decode


class TestLZSSFunctionality(unittest.TestCase):
    def test_simple_encode(self):
        test_string = bytearray(b'best test in bestest tester fest')
        result_string = b'\x0cbest t\t\x05\x06in \t\r\x11\x10\x08er f\x07\x07'
        self.assertEqual(lzss_encode(test_string), result_string)

    def test_buffer_size_affects_output(self):
        test_string = bytearray(b'test test golden retilou test')
        self.assertNotEqual(lzss_encode(test_string, 50),
                            lzss_encode(test_string, 5))

    def test_simple_decode(self):
        test_string = b'\x14test in a \t\n'
        result_string = bytearray(b'test in a test')
        self.assertEqual(lzss_decode(test_string), result_string)

    def test_simple_encode_decode(self):
        test_string = bytearray(b'testing a testy tester in a tester network of testers')
        self.assertEqual(lzss_decode(lzss_encode(test_string)), test_string)


if __name__ == '__main__':
    unittest.main()
