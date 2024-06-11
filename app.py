from flask import Flask, render_template, request, jsonify
import random
import json
import nltk

app = Flask(__name__)

# Load preprocessed data
with open('tokenized_pairs.json') as f:
    pairs = json.load(f)

def get_response(user_input):
    user_tokens = nltk.tokenize.word_tokenize(user_input.lower())
    for pair in pairs:
        question, answer = pair
        if set(user_tokens).intersection(set(question)):
            return ' '.join(answer)
    return "Sorry, I don't understand that."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response_route():
    user_message = request.json.get('message')
    response_message = get_response(user_message)
    return jsonify({'response': response_message})

if __name__ == '__main__':
    nltk.download('punkt')
    app.run(debug=True)
