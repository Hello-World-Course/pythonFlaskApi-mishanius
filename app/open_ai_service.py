import json
from app.NextMove import NextMove

CONTINUE_TAG = "CONTINUE"
YOU_LOST_TAG = "YOU_LOST"
YOU_WIN_TAG = "YOU_WIN"


def next_move(user_word, used_words):
    if used_words and user_word[0] != used_words[0][-1]:
        return NextMove(YOU_LOST_TAG, "",
                        f"You didn't choose a word that starts from the last letter of the previous word {used_words[-1]}")
    # Complete the rest
    # Placeholder for generating next word logic (Leave this comment for now)
