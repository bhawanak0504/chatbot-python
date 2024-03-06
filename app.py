from flask import Flask, render_template, request
import re
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        response = handle_user_input(user_input)
        return render_template('chatbot.html', response=response)
    else:
        return render_template('chatbot.html')

def handle_user_input(user_input):
    user_input = user_input.lower()

    # Define recognized words and long responses
    R_EATING = "I don't like eating anything because I'm a bot obviously!"
    R_ADVICE = "If I were you, I would go to the internet and type exactly what you wrote there!"
    recognized_words = {
        'hello': ['hi', 'hey', 'hello'],
        'how are you': ['fine' ,'good', 'great'],
        'eat': ['what', 'you', 'eat'],
        'advice': ['give', 'advice'],
        'help': ['can', 'you', 'help'],
        'bye': ['goodbye', 'see you later', 'cya']
    }

    single_response = True
    required_words = []

    # Check for long responses
    for key, value in recognized_words.items():
        if set(value).issubset(set(user_input.split())):
            return eval(f"{key.upper()}")

    # Check for single-word responses
    for word in user_input.split():
        if word in recognized_words:
            return random.choice(recognized_words[word])

    # Default response
    return "I'm sorry, I don't understand."

if __name__ == '__main__':
    app.run(debug=True)