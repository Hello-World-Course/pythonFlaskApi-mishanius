import unittest

from test_base.test_base import AssignmentTester


class NextMoveTests(AssignmentTester):

    def test_invalid_start_letter(self):
        from app.open_ai_service import next_move, CONTINUE_TAG, YOU_LOST_TAG
        result = next_move("egg", ["banana"])
        self.assertEqual(result.tag, YOU_LOST_TAG)
        self.assertIn("didn't choose a word", result.explanation)

    def test_duplicate_word(self):
        from app.open_ai_service import next_move, CONTINUE_TAG, YOU_LOST_TAG
        result = next_move("egg", ["apple", "egg"])
        self.assertEqual(result.tag, YOU_LOST_TAG)
        self.assertIn("already been used", result.explanation)

    def test_valid_move(self):
        from app.open_ai_service import next_move, CONTINUE_TAG, YOU_LOST_TAG
        result = next_move("gone", ["egg"])
        self.assertEqual(result.tag, CONTINUE_TAG)
        self.assertEqual(result.next_word, "example")


if __name__ == "__main__":
    unittest.main()
