import json
from app.NextMove import NextMove

CONTINUE_TAG = "CONTINUE"
YOU_LOST_TAG = "YOU_LOST"
YOU_WIN_TAG = "YOU_WIN"


def next_move(user_word, used_words):
    if used_words and user_word[0] != used_words[0][-1]:
        return NextMove(YOU_LOST_TAG, "",
                        f"You didn't choose a word that starts from the last letter of the previous word {used_words[-1]}")
    if user_word.strip().lower() in used_words:
        return NextMove(YOU_LOST_TAG, "", f"{user_word} has already been used")
    # Placeholder for generating next word logic
    return NextMove(CONTINUE_TAG, "example", "Explanation of the move")
