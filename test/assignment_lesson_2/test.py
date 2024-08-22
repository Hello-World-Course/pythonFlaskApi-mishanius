import unittest
from test_base.test_base import AssignmentTester


class RoutesTests(AssignmentTester):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from app import create_app
        cls.app = create_app()
        cls.app.testing = True
        cls.client = cls.app.test_client()

    def test_game_get(self):
        response = self.client.get('/game')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Word Chain Game', response.data)

    def test_restart(self):
        response = self.client.get('/restart')
        self.assertEqual(302, response.status_code)  # Should redirect


if __name__ == "__main__":
    unittest.main()
