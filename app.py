from flask import Flask, render_template, request, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
# dubug = DebugToolbarExtension(app)

from boggle import Boggle

boggle_game = Boggle()

@app.before_first_request
def create_board():
    if 'board' not in session:
        session['board'] = boggle_game.make_board()
    session['score'] = 0

@app.route('/')
def start_game():
    board = session['board']
    score = session['score']
    return render_template('index.html', board=board, score=score)

# endpoint to handle AJAX request
@app.route('/check-guess', methods=['POST'])
def check_guess():
    guess = request.form['guess']
    result = boggle_game.check_valid_word(session['board'], guess)

    if 'score' not in session:
        session['score'] = 0

    if result == 'ok':
        session['score'] += len(guess)
        session.modified = True

    #print(session['score'])
    return jsonify({'result': result, 'score': session['score']})

@app.route('/reshuffle', methods=['POST'])
def reshuffle():
    session['board'] = boggle_game.make_board()
    session['score'] = 0
    print(session['score'])
    return jsonify({'board': session['board']})