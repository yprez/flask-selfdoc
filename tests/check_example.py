import unittest

from examples.simple.blog import app as simple_app


class TestSimpleApp(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.app = simple_app
        self.client = self.app.test_client()

    def test_output(self):
        r = self.client.get("/doc")
        self.assertEqual(r.status_code, 200)
        data = r.data.decode('utf-8')
        with open("tests/files/simple.html") as f:
            expected = f.read()

        self.assertEqual(data, expected)


if __name__ == "__main__":
    unittest.main()
