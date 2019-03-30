import data
# import seaborn as sns
# import statsmodels.api as sm
import matplotlib.pyplot as plt

# train_X = data.symptom_data.drop(columns=['user_id', 'date', 'id'])
# train_y = data.symptom_data[['user_id']]

data.user_data["duration"] = data.user_data["end_date"] - data.user_data["start_date"]

data.user_data.head()
