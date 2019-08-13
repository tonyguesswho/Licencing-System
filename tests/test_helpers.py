import unittest
from utils.helpers import check_key


class HelperTest(unittest.TestCase):

    def test_check_key_invalid(self):
        """Test checking unavailble key throws error"""
        with self.assertRaises(KeyError) as error:
            check_key(None, 'item not found')
        self.assertEqual("'item not found'", str(error.exception))

    def test_check_key_valid(self):
        """Test available dictionary key"""
        self.assertEqual(check_key({"id": 1}, 'item not found'), None)


if __name__ == '__main__':
    unittest.main()
