import TEST_LOGGINGANDPDB
import unittest
from collections import Iterator
class Testpasical(unittest.TestCase):
    def test_init(self):
        b=TEST_LOGGINGANDPDB.pasical(1)
        self.assertEqual(b,[1])
        self.assertTrue(isinstance(b,list))
        b=TEST_LOGGINGANDPDB.pasical(2)
        self.assertEqual(b,[1,1])
        self.assertTrue(isinstance(b,list))
        b=TEST_LOGGINGANDPDB.pasical(4)
        self.assertEqual(b,[1,3,3,1])
        self.assertTrue(isinstance(b,list))
    def test_calculate(self):
        b=TEST_LOGGINGANDPDB.calculate(3)
        self.assertTrue(isinstance(b,Iterator))
        self.assertEqual(next(b),[1,2,1])
        with self.assertRaises(StopIteration):
            next(b)
        
    def test_keyerror(self):
        with self.assertRaises(ValueError):
            TEST_LOGGINGANDPDB.pasical("qq")
            
if __name__=="__main__":
    unittest.main()

                         
