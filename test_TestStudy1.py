import unittest
import TestStudy1  #needs to be same directory

class TestCalc(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(TestStudy1.add(10,5),15)
        self.assertEqual(TestStudy1.add(-1,1),0)
        self.assertEqual(TestStudy1.add(-1,-1),-2)

    def test_subtract(self):
        self.assertEqual(TestStudy1.subtract(10,5),5)
        self.assertEqual(TestStudy1.subtract(-1,1),-2)
        self.assertEqual(TestStudy1.subtract(-1,-1),0)

    def test_multiply(self):
        self.assertEqual(TestStudy1.multiply(10,5),50)
        self.assertEqual(TestStudy1.multiply(-1,1),-1)
        self.assertEqual(TestStudy1.multiply(-1,-1),1)

    def test_divide(self):
        self.assertEqual(TestStudy1.divide(10,5),2)
        self.assertEqual(TestStudy1.divide(-1,1),-1)
        self.assertEqual(TestStudy1.divide(-1,-1),1)
        self.assertEqual(TestStudy1.divide(3,2),1.5)
        self.assertRaises(ValueError, TestStudy1.divide,10,0)

        #using context manager to capature assertions
        with self.assertRaises(ValueError):
            TestStudy1.divide(10,0)


if __name__ == '__main__':
    unittest.main()