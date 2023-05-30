import openai
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import pandas as pd
import json
openai.api_key = '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'

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "http://localhost:8080"}})
CORS(app)
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

@app.route('/login', methods=['POST'])
def login():
    # Get the username and password from the request body
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Perform your login logic here
    # You can replace the following example with your own implementation
    if username == 'admin' and password == 'password':
        # Login successful
        return jsonify(success=True)
    else:
        # Login failed
        return jsonify(success=False)

def readcsv():
    data_frame = pd.read_csv('resource/dailyavg-2023-05-30.csv')
    data_frame = data_frame.iloc[3:]
    data_frame = data_frame.set_index(data_frame.columns[0])
    row_name = 'Innovative Village ต.ป่าแดด อ.เมือง จ.เชียงใหม่'
    column_name = 'Unnamed: 15'
    selected_data = data_frame.loc[row_name, column_name]
    print(selected_data)





# if __name__ == '__main__':
#     app.run(debug=True)