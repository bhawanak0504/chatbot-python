from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import re
import random
import boto3

app = Flask(__name__)

# Initialize AWS S3 client
s3 = boto3.client('s3')

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        # Check if the request is for uploading a file
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'})
            
            if file:
                # Secure filename to prevent directory traversal
                filename = secure_filename(file.filename)
                
                # Upload file to S3 bucket
                s3.upload_fileobj(file, 'your-s3-bucket-name', filename)
                
                return jsonify({'success': True, 'message': 'File uploaded successfully'})

        else:
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
    app.run(debug=True,host='0.0.0.0', port=80)