import unittest
from lzss import lzss_encode, lzss_decode

class TestLZSSFunctionality(unittest.TestCase):
    def test_simple_encode(self):
        test_string = "test in testing new string"
        result_string = "test in <0,4><5,2>g new <2,2>r<12,3>"
        self.assertEqual(lzss_encode(test_string), result_string)

    def test_simple_decode(self):
        test_string = "testing a <0,4>er"
        result_string = "testing a tester"
        self.assertEqual(lzss_decode(test_string), result_string)

    def test_simple_encode_decode(self):
        test_string = "testing a testy tester in a tester network of testers"
        self.assertEqual(lzss_decode(lzss_encode(test_string)), test_string)



if __name__ == '__main__':
    unittest.main()



#print(test_string)
#print(lzss_encode(test_string))
#print(lzss_decode(lzss_encode(test_string)))