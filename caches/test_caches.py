import caches
import unittest

class TestCaches(unittest.TestCase):

    def test_dict_of_lists(self):
        self.assertEqual({},
                         caches.dict_of_lists([],
                                              'k', 'v'))
        self.assertEqual({'a' : [1]},
                         caches.dict_of_lists([{'k' : 'a', 'v' : 1}],
                                              'k', 'v'))
        self.assertEqual({'a' : [1, 3], 'b' : [2, 4]},
                         caches.dict_of_lists([{'k' : 'a', 'v' : 1},
                                               {'k' : 'b', 'v' : 2},
                                               {'k' : 'a', 'v' : 3},
                                               {'k' : 'b', 'v' : 4}],
                                              'k', 'v'))
        self.assertEqual({'a' : [1, 3], 'b' : [2, 4]},
                         caches.dict_of_lists([{'k' : 'a', 'v' : 1},
                                               {'k' : 'b', 'v' : 2},
                                               {'k' : 'a', 'v' : 3},
                                               {'k' : 'b', 'v' : 4},
                                               {'x' : 'b', 'v' : 5},
                                               {'k' : 'a', 'x' : 6}],
                                              'k', 'v'))

    def test_dict_of_items(self):
        self.assertEqual({},
                         caches.dict_of_items([],
                                              'k', 'v'))
        self.assertEqual({'a' : 1},
                         caches.dict_of_items([{'k' : 'a', 'v' : 1}],
                                              'k', 'v'))
        self.assertEqual({'a' : 1, 'b' : 2},
                         caches.dict_of_items([{'k' : 'a', 'v' : 1},
                                               {'k' : 'b', 'v' : 2}],
                                              'k', 'v'))
        self.assertEqual({'a' : 1, 'b' : 2},
                         caches.dict_of_items([{'k' : 'a', 'v' : 1},
                                               {'k' : 'b', 'v' : 2},
                                               {'x' : 'a', 'v' : 3},
                                               {'k' : 'b', 'x' : 4}],
                                              'k', 'v'))

if __name__ == '__main__':
    unittest.main()
