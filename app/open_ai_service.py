import json
from app.NextMove import NextMove
from flask import current_app as app
import openai

CONTINUE_TAG = "CONTINUE"
YOU_LOST_TAG = "YOU_LOST"
YOU_WIN_TAG = "YOU_WIN"
SYSTEM_PROMPT = "Your system prompt here"

openai.api_key = app.config.get("OPENAI_API_KEY")
def next_move(user_word, used_words):
    if used_words and user_word[0] != used_words[0][-1]:
        return NextMove(YOU_LOST_TAG, "",
                        f"You didn't choose a word that starts from the last letter of the previous word {used_words[-1]}")
    if user_word.strip().lower() in used_words:
        return NextMove(YOU_LOST_TAG, "", f"{user_word} has already been used")
    # Placeholder for generating next word logic
    return NextMove(CONTINUE_TAG, "example", "Explanation of the move")


def generate_word(chosen_word, used_words):
    filtered_word = [word for word in used_words if word[0] == chosen_word[-1]]
    # Function to generate a word starting with the given letter using ChatGPT
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4" if you have access to it
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": f"word: {chosen_word}, letter: {chosen_word[-1]}, used_words: {filtered_word}"}
        ],
        max_tokens=50  # Adjust the number of tokens as needed
    )
    return response.choices[0].message.content.strip()