import openai
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
openai.api_key = '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'

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "http://localhost:8080"}})
@app.route('/chat', methods=['POST'])
def chat():
    # Parse the JSON input from the request body
    input_text = request.json['input_text']
    print(input_text)
    # Call the OpenAI GPT-3 API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
             {"role": "user", "content": input_text},
         ]
     )

    # Extract the generated response text from the API response
    result = ''
    for choice in response.choices:
        result += choice.message.content
    output_text = result
    return jsonify({'output_text': output_text})

if __name__ == '__main__':
    app.run(debug=True)