'''
Data Loading and Normalisation
'''

import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt


def dateparse(dates):
    new_dates = []
    for d in dates:
        try:
            if ("/" in d):
                if len(d.split("/")[2]) == 4:
                    new_dates.append(pd.datetime.strptime(d, '%d/%m/%Y'))
                else:
                    new_dates.append(pd.datetime.strptime(
                        d, '%d/%m/%y').strftime('%d/%m/%Y'))

            if ("-") in d:
                d = d[2:]
                new_dates.append(pd.datetime.strptime(d, '%y-%m-%d'))
        except:
            new_dates.append(np.nan)
    return new_dates


period_data = pd.read_csv(
    "data/Period.csv", parse_dates=['start_date', 'end_date'], date_parser=dateparse)
period_data.dropna(inplace=True)

symptom_data = pd.read_csv(
    "data/Symptom.csv", parse_dates=['date'], date_parser=dateparse)
symptom_data.dropna(inplace=True)


user_data = pd.read_csv(
    "data/User.csv", parse_dates=['dob'], date_parser=dateparse)

symptom_data.drop(columns=['id'], inplace=True)
period_data.drop(columns=['id'], inplace=True)

# Creation of the ultimate table
new_data = pd.merge(period_data, symptom_data,
                    left_on='User_id', right_on='user_id', how='inner')
new_data = pd.merge(new_data, user_data, left_on='User_id',
                    right_on='id', how='inner')
new_data.drop(columns=['User_id', 'id'], inplace=True)

new_data = new_data.query('end_date > start_date')
new_data["last_date"] = new_data["end_date"] + pd.to_timedelta(
    new_data["cycle_length_initial"], unit='D') - pd.to_timedelta(new_data["period_length_initial"], unit='D')
new_data["current_day"] = (
    abs((new_data["date"] - new_data['start_date']).dt.days))
new_data = new_data[new_data.current_day > 0]
new_data = new_data[new_data.current_day < new_data.cycle_length_initial]
new_data["stage"] = new_data["current_day"] / new_data["cycle_length_initial"]
