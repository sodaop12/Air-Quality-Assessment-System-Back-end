import openai
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
openai.api_key = ''

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
def submitcompact_data():
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
    max_value = np.max([row_values1, row_values2, row_values3])
    non_zero_values = [arr[arr != 0] for arr in [row_values1, row_values2, row_values3]]
    min_value = np.min(np.concatenate(non_zero_values))
    CGRS = ((calculateaverage/22)/24)*totalhour
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Average AQI = "+str(calculateaverage)+", Max AQI = "+str(max_value)+", Min AQI = "+str(min_value)+", Total Hours ="+str(totalhour)+
                                        " Please give Suggestions to this Patient According to the Patient's history and Assessment as a Doctor who directly works related to respiratory disease."
                                        " Each topic is limited to only 200 characters"
                                        "1. Diagnosis and Explanation"
                                        "2. Relate to Air Quality Index table"
                                        "3. Emphasizing Preventive Care"
                                        "4. Follow-up Plan"
                                        "5. Personalized Recommendations"
                                        "6. Give Details of suggestions as a doctor"
                                        },
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
        'output_text': output_text,
        'max': max_value,
        'min': min_value,
        'CGRS': CGRS
    }
    return jsonify(response_data), 200
@app.route('/submitcompletedata', methods=['POST'])
def submitcompelete_data():
    data_frame = pd.read_csv('resource/dailyavg-2023-05-30.csv')
    data_frame = data_frame.iloc[3:]
    data_frame = data_frame.set_index(data_frame.columns[0])
    data = request.json
    selected_days = data.get("selectedDays")
    additional_days = data.get("additionalDays")
    additional_start_date = data.get("additionalStartDate")
    additional_end_date = data.get("additionalEndDate")
    additional_hours = data.get("additionalHours")
    additional_text = data.get("additionalText")
    locations = data.get("locations")
    locations30 = data.get("locations30")
    averagehours = data.get("hours30")
    print(selected_days)
    print(additional_days)
    print(additional_start_date)
    print(additional_end_date)
    print(additional_hours)
    print(additional_text)
    print(locations)
    print(locations30)
    averageAQI = 0
    if selected_days <= 7:
        column_names = [f'Unnamed: {index}' for index in additional_days]
        row_names = locations
        sums = []
        for row_name, col_name in zip(row_names, column_names):
            value = data_frame.loc[row_name, col_name]
            sums.append(value)
        total_sum = sum(sums)
        averageAQI = total_sum/selected_days
        averageAQI_str = str(averageAQI)
        max_value = np.max([sums])
        min_value = np.min(sums)
        averagehours = sum(additional_hours)
        totalhour = selected_days * averagehours
        CGRS = ((averageAQI / 22) / 24) * totalhour
        print(sums)
        print(total_sum)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Average AQI = " + str(averageAQI) + ", Max AQI = " + str(
                    max_value) + ", Min AQI = " + str(min_value) + ", Total Hours =" + str(totalhour) + ", congenital disease ="+ str(additional_text) +
                                            " Please give Suggestions to this Patient According to the Patient's history and Assessment as a Doctor who directly works related to respiratory disease."
                                            " Each topic is limited to only 200 characters"
                                            "1. Diagnosis and Explanation"
                                            "2. Relate to Air Quality Index table"
                                            "3. Emphasizing Preventive Care"
                                            "4. Follow-up Plan"
                                            "5. Personalized Recommendations"
                                            "6. Give Details of suggestions as a doctor"
                 },
            ]
        )
        resultGPT = ''
        for choice in response.choices:
            resultGPT += choice.message.content
        output_text = resultGPT

    elif selected_days >7 and selected_days <=29:
        start = additional_start_date
        end = additional_end_date
        if start <= end:
           numbers = list(range(start, end + 1))
        else:
           numbers = list(range(start, end - 1, -1))
        column_names = [f'Unnamed: {index}' for index in numbers]
        row_values1 = data_frame.loc[locations30[0],column_names].apply(pd.to_numeric, errors='coerce').fillna(0)
        row_sum1 = np.sum(row_values1)
        row_values2 = data_frame.loc[locations30[1],column_names].apply(pd.to_numeric, errors='coerce').fillna(0)
        row_sum2 = np.sum(row_values2)
        row_values3 = data_frame.loc[locations30[2],column_names].apply(pd.to_numeric, errors='coerce').fillna(0)
        row_sum3 = np.sum(row_values3)
        averageAQI = ((row_sum1 / 30) + (row_sum2 / 30) + (row_sum3 / 30)) / 3
        totalhour = selected_days * averagehours
        max_value = np.max([row_values1, row_values2, row_values3])
        non_zero_values = [arr[arr != 0] for arr in [row_values1, row_values2, row_values3]]
        min_value = np.min(np.concatenate(non_zero_values))
        CGRS = ((averageAQI / 22) / 24) * totalhour
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Average AQI = " + str(averageAQI) + ", Max AQI = " + str(
                    max_value) + ", Min AQI = " + str(min_value) + ", Total Hours =" + str(
                    totalhour) + ", congenital disease =" + str(additional_text) +
                                            " Please give Suggestions to this Patient According to the Patient's history and Assessment as a Doctor who directly works related to respiratory disease."
                                            " Each topic is limited to only 200 characters"
                                            "1. Diagnosis and Explanation"
                                            "2. Relate to Air Quality Index table"
                                            "3. Emphasizing Preventive Care"
                                            "4. Follow-up Plan"
                                            "5. Personalized Recommendations"
                                            "6. Give Details of suggestions as a doctor"
                 },
            ]
        )
        resultGPT = ''
        for choice in response.choices:
            resultGPT += choice.message.content
        output_text = resultGPT

    elif selected_days == 30:
        row_values1 = data_frame.loc[locations30[0]].apply(pd.to_numeric, errors='coerce').fillna(0)
        row_sum1 = np.sum(row_values1)
        row_values2 = data_frame.loc[locations30[1]].apply(pd.to_numeric, errors='coerce').fillna(0)
        row_sum2 = np.sum(row_values2)
        row_values3 = data_frame.loc[locations30[2]].apply(pd.to_numeric, errors='coerce').fillna(0)
        row_sum3 = np.sum(row_values3)
        averageAQI = ((row_sum1 / 30) + (row_sum2 / 30) + (row_sum3 / 30)) / 3
        totalhour = 30 * averagehours
        max_value = np.max([row_values1, row_values2, row_values3])
        non_zero_values = [arr[arr != 0] for arr in [row_values1, row_values2, row_values3]]
        min_value = np.min(np.concatenate(non_zero_values))
        CGRS = ((averageAQI / 22) / 24) * totalhour
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Average AQI = " + str(averageAQI) + ", Max AQI = " + str(
                    max_value) + ", Min AQI = " + str(min_value) + ", Total Hours =" + str(
                    totalhour) + ", congenital disease =" + str(additional_text) +
                                            " Please give Suggestions to this Patient According to the Patient's history and Assessment as a Doctor who directly works related to respiratory disease."
                                            " Each topic is limited to only 200 characters"
                                            "1. Diagnosis and Explanation"
                                            "2. Relate to Air Quality Index table"
                                            "3. Emphasizing Preventive Care"
                                            "4. Follow-up Plan"
                                            "5. Personalized Recommendations"
                                            "6. Give Details of suggestions as a doctor"
                 },
            ]
        )
        resultGPT = ''
        for choice in response.choices:
            resultGPT += choice.message.content
        output_text = resultGPT

    response_data = {
        'success': 200,
        'calculateaverage': averageAQI,
        'totalhour': totalhour,
        'max': max_value,
        'min': min_value,
        'output_text': output_text,
        'CGRS': CGRS
    }
    return  jsonify(response_data), 200

if __name__ == '__main__':
    app.run()

def readcsv():
    data_frame = pd.read_csv('resource/dailyavg-2023-05-30.csv')
    data_frame = data_frame.iloc[3:]
    data_frame = data_frame.set_index(data_frame.columns[0])
    row_name1 = 'Innovative Village ต.ป่าแดด อ.เมือง จ.เชียงใหม่'
    row_name2 = 'คณะการสื่อสารมวลชน มช. ต.สุเทพ อ.เมือง จ.เชียงใหม่'
    row_name3 = 'คณะบริหารธุรกิจ มช. ต.สุเทพ อ.เมือง จ.เชียงใหม่'
    column_name = 'Unnamed: 15'
    row_values1 = data_frame.loc[row_name1].apply(pd.to_numeric, errors='coerce').fillna(0)
    row_values2 = data_frame.loc[row_name2].apply(pd.to_numeric, errors='coerce').fillna(0)
    row_values3 = data_frame.loc[row_name3].apply(pd.to_numeric, errors='coerce').fillna(0)
    max_value = np.max([row_values1, row_values2, row_values3])
    non_zero_values = [arr[arr != 0] for arr in [row_values1, row_values2, row_values3]]
    min_value = np.min(np.concatenate(non_zero_values))
    print("Maximum value:", max_value)
    print("Minimum value:", min_value)

def generate_numbers(start, end):
    if start <= end:
        numbers = list(range(start, end + 1))
    else:
        numbers = list(range(start, end - 1, -1))
    return numbers

start_num = 2
end_num = 15

result = generate_numbers(start_num, end_num)
print(result)







