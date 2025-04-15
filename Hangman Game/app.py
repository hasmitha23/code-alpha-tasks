from flask import Flask, render_template, jsonify, request, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session storage

@app.route('/')
def index():
    if 'win_streak' not in session:
        session['win_streak'] = 0  # Initialize win streak
    return render_template('index.html')

@app.route('/get_word')
def get_word():
    with open("words.txt", "r") as file:
        words = file.read().splitlines()
    if words:
        word = random.choice(words)
        return jsonify({"word": word, "win_streak": session.get('win_streak', 0)})  # Send win streak with word
    else:
        return jsonify({"error": "No words available"}), 500

@app.route('/update_streak', methods=['POST'])
def update_streak():
    session['win_streak'] = session.get('win_streak', 0) + 1  # Increase win streak
    session.modified = True  # Ensure session updates
    return jsonify({"win_streak": session['win_streak']})

@app.route('/reset_streak', methods=['POST'])
def reset_streak():
    session['win_streak'] = 0  # Reset win streak on loss
    session.modified = True
    return jsonify({"win_streak": 0})

if __name__ == '__main__':
    app.run(debug=True)
