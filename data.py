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
                if len(d.split("/")[2])==4:
                    new_dates.append(pd.datetime.strptime(d, '%d/%m/%Y'))
                else:
                    new_dates.append(pd.datetime.strptime(d,'%d/%m/%y').strftime('%d/%m/%Y'))
            
            if ("-") in d:
                d = d[2:]
                new_dates.append(pd.datetime.strptime(d, '%y-%m-%d'))
        except:
            new_dates.append(np.nan)
    return new_dates


period_data = pd.read_csv("data/Period.csv",parse_dates=['start_date','end_date'], date_parser=dateparse) 
period_data.dropna(inplace=True)

symptom_data = pd.read_csv("data/Symptom.csv",parse_dates=['date'], date_parser=dateparse) 
symptom_data.dropna(inplace=True)


user_data = pd.read_csv("data/User.csv",parse_dates=['dob'], date_parser=dateparse)

symptom_data.drop(columns=['id'], inplace=True)
period_data.drop(columns=['id'], inplace=True)


