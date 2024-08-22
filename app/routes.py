from flask import request, session, redirect, url_for
from flask import current_app as app, render_template


@app.route('/game', methods=['GET'])
def game():
    return render_template('game.html', words=session.get('used_words', []))

@app.route('/restart', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('game'))