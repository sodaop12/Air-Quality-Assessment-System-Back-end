import openai
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import pandas as pd
import numpy as np
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
@app.route('/submitcompactdata', methods=['POST'])
def submit_data():
    data_frame = pd.read_csv('resource/dailyavg-2023-05-30.csv')
    data_frame = data_frame.iloc[3:]
    data_frame = data_frame.set_index(data_frame.columns[0])
    data = request.get_json()
    # Access the collected data
    locations = data['locations']
    selectedDays = data['selectedDays']
    averageHours = data['averageHours']
    row_values1 = data_frame.loc[locations[0]].apply(pd.to_numeric, errors='coerce').fillna(0)
    row_sum1 = np.sum(row_values1)
    row_values2 = data_frame.loc[locations[1]].apply(pd.to_numeric, errors='coerce').fillna(0)
    row_sum2 = np.sum(row_values2)
    row_values3 = data_frame.loc[locations[2]].apply(pd.to_numeric, errors='coerce').fillna(0)
    row_sum3 = np.sum(row_values3)
    calculateaverage = ((row_sum1/30)+(row_sum2/30)+(row_sum3/30))/3
    totalhour = selectedDays*averageHours
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "if i receive average AQI "
            +str(calculateaverage)+"and i receive it for"+str(totalhour)+" is it affect my health and do you have any suggestion for me"},
        ]
    )
    resultGPT = ''
    for choice in response.choices:
        resultGPT += choice.message.content
    output_text = resultGPT
    print(output_text)
    response_data = {
        'calculateaverage': calculateaverage,
        'totalhour': totalhour,
        'output_text': output_text
    }
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run()

def readcsv():
    data_frame = pd.read_csv('resource/dailyavg-2023-05-30.csv')
    data_frame = data_frame.iloc[3:]
    data_frame = data_frame.set_index(data_frame.columns[0])
    row_name = 'Innovative Village ต.ป่าแดด อ.เมือง จ.เชียงใหม่'
    column_name = 'Unnamed: 15'
    row_values = data_frame.loc[row_name].apply(pd.to_numeric, errors='coerce').fillna(0)
    row_sum = np.sum(row_values)
    result = f"Row: {row_name}, Sum: {row_sum}"
    print(result)






# if __name__ == '__main__':
#     app.run(debug=True)