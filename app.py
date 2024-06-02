from flask import Flask, request, render_template, jsonify, session 
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = 'hushHushHush'

boggle_game = Boggle()

@app.route("/")
def homepage():
    """Create and display board."""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 0)

    return render_template("index.html", board = board, highscore = highscore, num_plays = num_plays)


@app.route("/check-word")
def check_word():
    """Check if word on the board."""
    guess_word = request.args.get('word')
    board = session.get('board')
    result = boggle_game.check_valid_word(board, guess_word)

    return jsonify({'result': result })


@app.route("/final-score", methods=["POST"])
def final_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    print(score)
    highscore = session.get("highscore", 0)
    print(highscore)
    num_plays = session.get("num_plays", 0)
    print(num_plays)

    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(newRecord=score > highscore)