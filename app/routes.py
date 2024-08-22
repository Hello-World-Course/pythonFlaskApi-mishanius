from flask import request, session, redirect, url_for
from flask import current_app as app, render_template


@app.route('/FIXME_WRONG_END_POINT', methods=['FIXME_WRONG_METHODS'])
def game():
    if request.method == 'POST':
        # add logic for words
    return render_template('game.html', words=session.get('used_words', []))


# add restart route here
