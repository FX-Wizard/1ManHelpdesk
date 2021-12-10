import unittest
import os
import configini

class TestINIParser(unittest.TestCase):
    testDict = {
        'key1': 1,
        'key2': 'two'
    }

    def test_createINIFile(self):
        config = configini.INIHandler('test.ini')
        config.save()
        self.assertTrue(os.path.isfile('test.ini'))


    def test_convertDictToINI(self):
        config = configini.INIHandler('test.ini')
        config.ini.test.data = ('test')
        config.save()


if __name__ == '__main__':
    unittest.main()