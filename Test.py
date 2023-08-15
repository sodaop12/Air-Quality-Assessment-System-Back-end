import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
def submitcompact_data():
  data_frame = pd.read_csv('resource/dailyavg-2023-05-30.csv')
  data_frame = data_frame.iloc[3:]
  data_frame = data_frame.set_index(data_frame.columns[0])
  print(data_frame)
  row_name1 = 'Innovative Village ต.ป่าแดด อ.เมือง จ.เชียงใหม่'
  data = data_frame.loc[row_name1].apply(pd.to_numeric, errors='coerce').fillna(0)
  print(data)
  X = np.arange(1, len(data) + 1).reshape(-1, 1)
  y = np.array(data)

  # Create and train the linear regression model
  model = LinearRegression()
  model.fit(X, y)

  # Predict the next number
  next_number = model.predict([[len(data) + 1]])[0]
  print("Predicted next number:", next_number)
