import unittest
from unittest.mock import patch, Mock

from app import create_app


class StaticFilesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.testing = True
        cls.client = cls.app.test_client()

    def setUp(self):
        # before each test we need to restart the session
        self.client.get('/restart')

    def test_css(self):
        response = self.client.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'body', response.data)

    def test_css_on_game(self):
        response = self.client.get('/game')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'href="/static/css/style.css"', response.data)

    def test_css_on_game_over(self):
        response = self.client.get('/game')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'href="/static/css/style.css"', response.data)

    def test_full_game_same_word_twice(self):
        with self.app.app_context() as appContext:
            with patch('app.open_ai_service.openai.chat.completions.create') as mock_openai:
                appContext.app.config.__setitem__("OPENAI_API_KEY", "fake_api_key")
                content = Mock(content='{"tag": "CONTINUE", "word": "era", "explanation": "Example explanation"}')
                choice = Mock(message=content)
                mock_openai.return_value.choices = [choice]
                # go to page game
                response = self.client.get('/game')
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Word Chain Game', response.data)
                # send apple
                response = self.client.post('/game', data={'user_word': 'apple'}, follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                # verify era was returned
                self.assertIn(b'era', response.data)
                # verify apple is shown
                self.assertIn(b'apple', response.data)
                # verify we are on the correct page
                self.assertIn(b'Word Chain Game', response.data)
                # send apple again
                response = self.client.post('/game', data={'user_word': 'apple'}, follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'apple has already been used', response.data)

    def test_full_game_not_starting_from_letter(self):
        with self.app.app_context() as appContext:
            with patch('app.open_ai_service.openai.chat.completions.create') as mock_openai:
                appContext.app.config.__setitem__("OPENAI_API_KEY", "fake_api_key")
                content = Mock(content='{"tag": "CONTINUE", "word": "era", "explanation": "Example explanation"}')
                choice = Mock(message=content)
                mock_openai.return_value.choices = [choice]
                # go to page game
                response = self.client.get('/game')
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Word Chain Game', response.data)
                # send apple
                response = self.client.post('/game', data={'user_word': 'apple'}, follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                # verify apple is shown
                self.assertIn(b'apple', response.data)
                # verify era was returned
                self.assertIn(b'era', response.data)
                # verify we are on the correct page
                self.assertIn(b'Word Chain Game', response.data)
                # send wrong word not starting with correct letter
                response = self.client.post('/game', data={'user_word': 'wrong'}, follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'choose a word that starts from the last letter of the previous word apple', response.data)

if __name__ == "__main__":
    unittest.main()
