import service
import unittest

class TestService(unittest.TestCase):

    def test_get_valid_threshold_none(self):
        self.assertEqual(20, service.get_valid_threshold(None))

    def test_get_valid_threshold_invalid_type(self):
        with self.assertRaises(service.ThresholdNotAnIntegerException):
            service.get_valid_threshold('foobar')

    def test_get_valid_threshold_invalid_number(self):
        with self.assertRaises(service.ThresholdOutOfRangeException):
            service.get_valid_threshold(-10)
        with self.assertRaises(service.ThresholdOutOfRangeException):
            service.get_valid_threshold(0)

    def test_get_valid_threshold_valid_number(self):
        self.assertEqual(1, service.get_valid_threshold(1))
        self.assertEqual(50, service.get_valid_threshold(50))
        self.assertEqual(200, service.get_valid_threshold(200))
        self.assertEqual(42, service.get_valid_threshold(42.1))
        self.assertEqual(42, service.get_valid_threshold(42.5))
        self.assertEqual(42, service.get_valid_threshold(42.9))

if __name__ == '__main__':
    unittest.main()
