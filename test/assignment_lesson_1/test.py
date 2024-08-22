import unittest

from test_base.test_base import AssignmentTester


class BasicTests(AssignmentTester):

    def setUp(self):
        # setup code
        from app import create_app
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_home(self):
        # test
        ######
        response = self.client.get('/')
        # verify
        self.assertEqual(response.status_code, 404)  # No route yet, should return 404


if __name__ == "__main__":
    unittest.main()