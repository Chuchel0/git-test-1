import unittest
from fibonacci import is_fibonacci

class TestFibonacci(unittest.TestCase):

    def test_fibonacci_numbers(self):
        self.assertEqual(is_fibonacci(0), (True, 0))
        self.assertEqual(is_fibonacci(1), (True, 1))
        self.assertEqual(is_fibonacci(2), (True, 3))
        self.assertEqual(is_fibonacci(3), (True, 4))
        self.assertEqual(is_fibonacci(5), (True, 5))
        self.assertEqual(is_fibonacci(8), (True, 6))
        self.assertEqual(is_fibonacci(13), (True, 7))
        self.assertEqual(is_fibonacci(21), (True, 8))

    def test_non_fibonacci_numbers(self):
        self.assertEqual(is_fibonacci(4), (False, -1))
        self.assertEqual(is_fibonacci(6), (False, -1))
        self.assertEqual(is_fibonacci(7), (False, -1))
        self.assertEqual(is_fibonacci(9), (False, -1))
        self.assertEqual(is_fibonacci(10), (False, -1))

    def test_negative_numbers(self):
        self.assertEqual(is_fibonacci(-1), (False, -1))
        self.assertEqual(is_fibonacci(-5), (False, -1))

if __name__ == '__main__':
    unittest.main()
