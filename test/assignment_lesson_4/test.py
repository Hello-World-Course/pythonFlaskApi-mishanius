import unittest
from unittest.mock import patch, Mock

from flask import Flask

from test_base.test_base import AssignmentTester


class OpenAIServiceTests(AssignmentTester):
    app = Flask('test')

    def test_next_move(self):
        with self.app.app_context():
            with patch('app.open_ai_service.generate_word') as mock_generate_word:
                from app.open_ai_service import next_move, CONTINUE_TAG
                mock_generate_word.return_value = '{"tag": "CONTINUE", "word": "example", "explanation": "Example explanation"}'
                result = next_move("apple", [])
                self.assertEqual(result.tag, CONTINUE_TAG)
                self.assertEqual(result.next_word, "example")

    def test_next_move_already_used(self):
        with self.app.app_context():
            with patch('app.open_ai_service.generate_word') as mock_generate_word:
                from app.open_ai_service import next_move, YOU_LOST_TAG
                result = next_move("apple", ["era", "apple"])
                self.assertEqual(result.tag, YOU_LOST_TAG)
                self.assertEqual(result.explanation, "apple has already been used")

    def test_next_move_not_starting_from_letter(self):
        with self.app.app_context():
            with patch('app.open_ai_service.generate_word') as mock_generate_word:
                from app.open_ai_service import next_move, YOU_LOST_TAG
                result = next_move("apple", ["not"])
                self.assertEqual(result.tag, YOU_LOST_TAG)
                self.assertEqual(result.explanation, "You didn't choose a word that starts from the last letter of the previous word not")

    def test_generate_word(self):
        with self.app.app_context() as appContext:
            appContext.app.config.__setitem__("OPENAI_API_KEY", "fake_api_key")
            with patch('app.open_ai_service.openai.chat.completions.create') as mock_openai:
                from app.open_ai_service import generate_word
                content = Mock(content='{"tag": "CONTINUE", "word": "era", "explanation": "Example explanation"}')
                choice = Mock(message=content)
                mock_openai.return_value.choices = [choice]
                result = generate_word("apple", [])
                self.assertIn('"tag": "CONTINUE"', result)

    def test_verify_filter_in_generate_word(self):
        with self.app.app_context() as appContext:
            appContext.app.config.__setitem__("OPENAI_API_KEY", "fake_api_key")
            with patch('app.open_ai_service.openai.chat.completions.create') as mock_openai:
                from app.open_ai_service import generate_word
                content = Mock(content='{"tag": "CONTINUE", "word": "era", "explanation": "Example explanation"}')
                choice = Mock(message=content)
                mock_openai.return_value.choices = [choice]
                result = generate_word("apple", ["era", "test", "bomb", "egg"])
                call_to_open_ai_parameters = mock_openai.call_args.kwargs
                user_role_input = next(filter(lambda a: a['role'] == 'user', call_to_open_ai_parameters['messages']))['content']
                self.assertIn('era', user_role_input)
                self.assertIn('egg', user_role_input)
                self.assertNotIn("test", user_role_input)
                self.assertNotIn("bomb", user_role_input)


if __name__ == "__main__":
    unittest.main()
