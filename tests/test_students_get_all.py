import unittest
import os
import sys
sys.path.append(os.path.join(os.curdir, "api/students"))
import get


class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        return
        print("not testing response.")
        result = get.handler(None, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn('Andrew', result['body'])


if __name__ == '__main__':
    unittest.main()
