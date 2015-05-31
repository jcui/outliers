import detection
import unittest

class TestDetection(unittest.TestCase):

    def test_make_dict_subset(self):
        self.assertEqual({},
                         detection.make_dict_subset([],
                                                    {}))
        self.assertEqual({},
                         detection.make_dict_subset(['a'],
                                                    {'b' : 2}))
        self.assertEqual({'a' : 1},
                         detection.make_dict_subset(['a'],
                                                    {'a' : 1, 'b' : 2}))
        self.assertEqual({'a' : 1, 'b' : 2},
                         detection.make_dict_subset(['a', 'b'],
                                                    {'a' : 1, 'b' : 2}))
        self.assertEqual({'b' : 2, 'd' : 4},
                         detection.make_dict_subset(['a', 'b', 'c', 'd'],
                                                    {'b' : 2, 'd' : 4}))

    def test_is_outlier(self):
        self.assertFalse(detection.is_outlier(10, 10, 20))
        self.assertFalse(detection.is_outlier(8, 10, 30))
        self.assertFalse(detection.is_outlier(10, 8, 30))
        self.assertFalse(detection.is_outlier(1, 10, 90))
        self.assertFalse(detection.is_outlier(10, 0, 90))
        self.assertTrue(detection.is_outlier(7, 10, 20))
        self.assertTrue(detection.is_outlier(10, 7, 20))
        self.assertTrue(detection.is_outlier(4, 10, 50))
        self.assertTrue(detection.is_outlier(10, 1, 90))
        self.assertTrue(detection.is_outlier(0, 10, 90))

    def check_outliers_found(self, input_dict, threshold):
        average = sum(input_dict.values()) / len(input_dict)
        result_dict = detection.find_outlier_throughputs(input_dict,
                                                         average,
                                                         threshold)
        for key, value in input_dict.iteritems():
            if key in result_dict:
                self.assertTrue(detection.is_outlier(value, average, threshold))
            else:
                self.assertFalse(detection.is_outlier(value, average, threshold))

    def test_find_outlier_throughputs(self):
        input_dict = {'a' : 10}
        self.check_outliers_found(input_dict, 20)
        input_dict = {'a' : 10, 'b' : 8}
        self.check_outliers_found(input_dict, 5)
        input_dict = {'a' : 10, 'b' : 8}
        self.check_outliers_found(input_dict, 20)
        input_dict = {'a' : 10, 'b' : 8}
        self.check_outliers_found(input_dict, 40)
        input_dict = {'a' : 10, 'b' : 8, 'c' : 6, 'd': 4}
        self.check_outliers_found(input_dict, 1)
        input_dict = {'a' : 10, 'b' : 8, 'c' : 6, 'd': 4}
        self.check_outliers_found(input_dict, 5)
        input_dict = {'a' : 10, 'b' : 8, 'c' : 6, 'd': 4}
        self.check_outliers_found(input_dict, 10)
        input_dict = {'a' : 10, 'b' : 8, 'c' : 6, 'd': 4}
        self.check_outliers_found(input_dict, 20)
        input_dict = {'a' : 10, 'b' : 8, 'c' : 6, 'd': 4}
        self.check_outliers_found(input_dict, 50)
        input_dict = {'a' : 10, 'b' : 8, 'c' : 6, 'd': 4}
        self.check_outliers_found(input_dict, 99)

    def test_find_outliers(self):
        self.assertEqual(({}, 0),
                         detection.find_outliers([],
                                                 {},
                                                 20))
        self.assertEqual(({}, 10),
                         detection.find_outliers(['a'],
                                                 {'a' : 10},
                                                 20))
        self.assertEqual(({}, 8),
                         detection.find_outliers(['a', 'b', 'c'],
                                                 {'a' : 10, 'b' : 8, 'c' : 6},
                                                 40))
        self.assertEqual(({'a' : 10, 'c' : 6}, 8),
                         detection.find_outliers(['a', 'b', 'c'],
                                                 {'a' : 10, 'b' : 8, 'c' : 6},
                                                 20))
        self.assertEqual(({'a' : 10, 'b' : 5, 'c' : 3}, 6),
                         detection.find_outliers(['a', 'b', 'c'],
                                                 {'a' : 10, 'b' : 5, 'c' : 3},
                                                 10))
        self.assertEqual(({'a' : 10, 'c' : 3}, 6),
                         detection.find_outliers(['a', 'b', 'c'],
                                                 {'a' : 10, 'b' : 5, 'c' : 3},
                                                 20))
        self.assertEqual(({'a' : 10}, 6),
                         detection.find_outliers(['a', 'b', 'c'],
                                                 {'a' : 10, 'b' : 5, 'c' : 3},
                                                 60))
        self.assertEqual(({}, 6),
                         detection.find_outliers(['a', 'b', 'c'],
                                                 {'a' : 10, 'b' : 5, 'c' : 3},
                                                 80))
        self.assertEqual(({'b' : 8, 'c' : 6}, 7),
                         detection.find_outliers(['c', 'b', 'x'],
                                                 {'a' : 10, 'b' : 8, 'c' : 6},
                                                 5))

if __name__ == '__main__':
    unittest.main()
